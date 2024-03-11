import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from topicaxisapi.api import dependencies
from topicaxisapi.models import Channels
from topicaxisapi.repositories.sqlalchemy.channels import ChannelRepository
from topicaxisapi.services.channels.list_channels.service import ListChannels

logger = logging.getLogger(__name__)
router = APIRouter(dependencies=[Depends(dependencies.get_api_key)])


@router.get(
    "/v2/channels",
    tags=["channels"],
    summary="Get the channels",
    description="Get the available channels",
)
def get_channels(
    session: Session = Depends(dependencies.get_session),
) -> Channels:
    channel_repository = ChannelRepository(session)
    list_channels = ListChannels(channel_repository)

    return list_channels.run()
