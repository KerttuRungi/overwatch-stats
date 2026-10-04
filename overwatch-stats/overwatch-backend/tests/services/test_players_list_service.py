from unittest.mock import MagicMock

import pytest

from models.player import Players
from schemas import PlayerProfileSummary
from services.players_list_service import PlayersService


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def service(repository):
    return PlayersService(repository)


@pytest.fixture
def player_data():
    return PlayerProfileSummary(username="Tracer", avatar="avatar.png", namecard="namecard.png")


def test_add_player_to_comparison_list(service, repository, player_data):
    repository.get_player_by_user.return_value = None

    result = service.add_comparison_player(player_data)

    saved_player = repository.add.call_args.args[0]
    assert isinstance(saved_player, Players)
    assert saved_player.username == "Tracer"
    assert saved_player.avatar == "avatar.png"
    assert saved_player.namecard == "namecard.png"
    assert result == repository.add.return_value


def test_add_dublicate_comparison_player(service, repository, player_data):
    repository.get_player_by_user.return_value = Players(username="Tracer", avatar="a", namecard="n")

    with pytest.raises(ValueError):
        service.add_comparison_player(player_data)

    repository.add.assert_not_called()


def test_get_all_players_returns_summaries(service, repository):
    repository.get_all_players.return_value = [
        Players(id=1, username="Tracer", avatar="a1", namecard="n1"),
        Players(id=2, username="Mercy", avatar="a2", namecard="n2"),
    ]

    result = service.get_all_players()

    assert result == [
        PlayerProfileSummary(username="Tracer", avatar="a1", namecard="n1"),
        PlayerProfileSummary(username="Mercy", avatar="a2", namecard="n2"),
    ]


def test_get_all_players_returns_empty_list(service, repository):
    repository.get_all_players.return_value = []

    assert service.get_all_players() == []


def test_remove_comparison_player_deletes_existing_player(service, repository):
    player = Players(id=1, username="Tracer", avatar="a", namecard="n")
    repository.get_player_by_user.return_value = player

    result = service.remove_comparison_player("Tracer")

    repository.delete.assert_called_once_with(player)
    assert result == PlayerProfileSummary(username="Tracer", avatar="a", namecard="n")


def test_remove_comparison_player_rejects_missing_player(service, repository):
    repository.get_player_by_user.return_value = None

    with pytest.raises(ValueError):
        service.remove_comparison_player("Tracer")

    repository.delete.assert_not_called()
