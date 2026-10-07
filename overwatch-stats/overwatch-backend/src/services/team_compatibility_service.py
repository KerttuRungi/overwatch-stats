from collections import Counter

from schemas import (
    PlayerRoleProfile,
    RoleAssignment,
    RoleSuggestion,
    TeamCompatibilityResponse,
)

SLOTS = {"tank": 1, "damage": 2, "support": 2}
TEAM_SIZE = sum(SLOTS.values())


def fit(profile: PlayerRoleProfile, role: str) -> float:
    """Share of the player's main role hours they have on `role` (1.0 on their main role)."""
    return profile.role_hours.get(role, 0) / profile.role_hours[profile.main_role]


def assign_roles(profiles: list[PlayerRoleProfile]) -> list[RoleAssignment]:
    """Seat min(n, 5) players in the 1 tank / 2 damage / 2 support slots, maximising total fit."""
    roles = list(SLOTS)
    seats = min(len(profiles), TEAM_SIZE)

    # state: seats used per role -> (total fit, assignments so far)
    states: dict[tuple[int, ...], tuple[float, list[RoleAssignment]]] = {(0, 0, 0): (0.0, [])}
    for profile in profiles:
        next_states = dict(states)  # the player may also sit out
        for used, (total, assigned) in states.items():
            for index, role in enumerate(roles):
                if used[index] >= SLOTS[role]:
                    continue
                key = used[:index] + (used[index] + 1,) + used[index + 1:]
                value = fit(profile, role)
                if key not in next_states or total + value > next_states[key][0]:
                    assignment = RoleAssignment(
                        username=profile.username,
                        assigned_role=role,
                        main_role=profile.main_role,
                        fit=round(value, 2),
                    )
                    next_states[key] = (total + value, assigned + [assignment])
        states = next_states

    full = [state for used, state in states.items() if sum(used) == seats]
    return max(full, key=lambda state: state[0])[1]


def check_compatibility(profiles: list[PlayerRoleProfile]) -> TeamCompatibilityResponse:
    eligible = [profile for profile in profiles if profile.main_role]
    assignments = assign_roles(eligible)

    seated = {assignment.username for assignment in assignments}
    filled = Counter(assignment.assigned_role for assignment in assignments)
    open_slots = [role for role, count in SLOTS.items() for _ in range(count - filled[role])]
    substitutes = [profile.username for profile in eligible if profile.username not in seated]

    by_name = {profile.username: profile for profile in eligible}
    warnings = [
        f"{count} players main {role}, only {SLOTS[role]} {role} slot{'s' if SLOTS[role] > 1 else ''}."
        for role, count in Counter(profile.main_role for profile in eligible).items()
        if count > SLOTS[role]
    ]
    suggestions = [
        RoleSuggestion(
            username=assignment.username,
            from_role=assignment.main_role,
            to_role=assignment.assigned_role,
            fit=assignment.fit,
            message=_suggestion_message(by_name[assignment.username], assignment),
        )
        for assignment in assignments
        if assignment.assigned_role != assignment.main_role
    ]

    score = round(100 * sum(a.fit for a in assignments) / len(assignments)) if assignments else 0
    return TeamCompatibilityResponse(
        players=profiles,
        assignments=assignments,
        open_slots=open_slots,
        substitutes=substitutes,
        score=score,
        compatible=bool(assignments) and not suggestions,
        warnings=warnings,
        suggestions=suggestions,
    )


def _suggestion_message(profile: PlayerRoleProfile, assignment: RoleAssignment) -> str:
    hours = profile.role_hours.get(assignment.assigned_role, 0)
    if hours == 0:
        return f"{profile.username} ({assignment.main_role} main) could be asked to try {assignment.assigned_role}, no hours there yet."
    return (
        f"{profile.username} ({assignment.main_role} main) could flex to {assignment.assigned_role}: "
        f"{assignment.fit:.0%} of their {assignment.main_role} hours ({hours:.0f}h played)."
    )
