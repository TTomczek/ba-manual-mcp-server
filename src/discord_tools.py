from datetime import datetime
from enum import Enum
from typing import Annotated, Dict, Any, Optional

from pydantic import Field, BaseModel

from server import mcp
from src.discord_client import CreateThreadRequest
from src.discord_client.api.default_api import DefaultApi
from src.discord_client.api_client import ApiClient
from src.discord_client.configuration import Configuration

config = Configuration(
    host = "https://discord.com/api/v10"
)
api_client = ApiClient(configuration=config)
api = DefaultApi(api_client=api_client)

snowflake_pattern = "^(0|[1-9][1-9]*)$"

@mcp.tool()
async def list_my_guilds(before: Annotated[Optional[str], Field(pattern=snowflake_pattern)] = None, after: Annotated[Optional[str], Field(pattern=snowflake_pattern)] = None, limit: Annotated[Optional[int], Field(gt=0,le=200)] = None, with_counts: Optional[bool] = None):
    guilds = await api.list_my_guilds(before=before, after=after, limit=limit, with_counts=with_counts)
    return guilds

@mcp.tool()
async def list_guild_channels(guild_id: Annotated[str, Field(pattern=snowflake_pattern)]):
    channels = await api.list_guild_channels(guild_id=guild_id)
    return channels

@mcp.tool()
async def list_messages(around: Annotated[Optional[str], Field(pattern=snowflake_pattern)] = None, before: Annotated[Optional[str], Field(pattern=snowflake_pattern)] = None, after: Annotated[Optional[str], Field(pattern=snowflake_pattern)] = None, limit: Annotated[Optional[int], Field(gt=0,le=100)] = None):
    messages = await api.list_messages(around=around, before=before, after=after, limit=limit)
    return messages


class ThreadAutoArchiveDuration(Enum):
    ONE_HOUR = 60
    ONE_DAY = 1440
    THREE_DAY = 4320
    SEVEN_DAY = 10080


class RichEmbedAuthor(BaseModel):
    name: Annotated[str, Field(max_length=256)] = None
    url: Annotated[str, Field(max_length=2048)] = None
    icon_url: Annotated[str, Field(max_length=2048)] = None


class RichEmbedField(BaseModel):
    name: Annotated[str, Field(max_length=256)]
    value: Annotated[str, Field(max_length=1024)]
    inline: bool | None = None


class RichEmbedFooter(BaseModel):
    text: Annotated[str, Field(max_length=2048)] = None
    icon_url: Annotated[str, Field(max_length=2048)] = None


class RichEmbedImage(BaseModel):
    url: Annotated[str, Field(max_length=2048)] = None
    width: int | None = None
    height: int | None = None
    placeholder: Annotated[str, Field(max_length=64)] = None
    placeholder_version: Annotated[int, Field(le=2147483647, ge=0)] = None
    is_animated: bool | None = None
    description: Annotated[str, Field(max_length=4096)] = None


class RichEmbedProvider(BaseModel):
    name: Annotated[str, Field(max_length=256)] = None
    url: Annotated[str, Field(max_length=2048)] = None


class RichEmbedThumbnail(BaseModel):
    url: Annotated[str, Field(max_length=2048)] = None
    width: int | None = None
    height: int | None = None
    placeholder: Annotated[str, Field(max_length=64)] = None
    placeholder_version: Annotated[int, Field(le=2147483647, ge=0)] = None
    is_animated: bool | None = None
    description: Annotated[str, Field(max_length=4096)] = None


class RichEmbedVideo(BaseModel):
    url: Annotated[str, Field(max_length=2048)] = None
    width: int | None = None
    height: int | None = None
    placeholder: Annotated[str, Field(max_length=64)] = None
    placeholder_version: Annotated[int, Field(le=2147483647, ge=0)] = None
    is_animated: bool | None = None
    description: Annotated[str, Field(max_length=4096)] = None


class RichEmbed(BaseModel):
    type: Annotated[str, Field(max_length=152133)] = None
    url: Annotated[str, Field(max_length=2048)] = None
    title: Annotated[str, Field(max_length=256)] = None
    color: Annotated[int, Field(le=16777215, ge=0)] = None
    timestamp: datetime = None
    description: Annotated[str, Field(max_length=4096)] = None
    author: RichEmbedAuthor = None
    image: RichEmbedImage = None
    thumbnail: RichEmbedThumbnail = None
    footer: RichEmbedFooter = None
    fields: Annotated[list[RichEmbedField], Field(max_length=25)] = None
    provider: RichEmbedProvider = None
    video: RichEmbedVideo = None


class MessageAllowedMentionsRequest(BaseModel):
    parse: Annotated[list[str], Field(max_length=1521)] = None
    users: Annotated[list[Annotated[str, Field(strict=True)]], Field(max_length=100)] = None
    roles: Annotated[list[Annotated[str, Field(strict=True)]], Field(max_length=100)] = None
    replied_user: bool | None = None


class MessageAttachmentRequest(BaseModel):
    id: Annotated[str, Field(strict=True)]
    filename: Annotated[str, Field(max_length=1024)] = None
    description: Annotated[str, Field(max_length=1024)] = None
    duration_secs: Annotated[float | int, Field(le=2147483647, ge=0)] = None
    waveform: Annotated[str, Field(max_length=400)] = None
    title: Annotated[str, Field(max_length=1024)] = None
    is_remix: bool | None = None


class CustomClientThemeShareRequest(BaseModel):
    colors: Annotated[list[Annotated[str, Field(min_length=6, max_length=6)]], Field(min_length=1, max_length=5)]
    gradient_angle: Annotated[int, Field(le=360, ge=0)]
    base_mix: Annotated[int, Field(le=100, ge=0)]
    base_theme: int | None = None


class PollEmoji(BaseModel):
    id: Annotated[str, Field(strict=True)] = None
    name: Annotated[str, Field(max_length=32)] = None
    animated: bool | None = None


class PollMedia(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=300)] = None
    emoji: PollEmoji = None


class PollEmojiCreateRequest(BaseModel):
    id: Annotated[str, Field(strict=True)] = None
    name: Annotated[str, Field(max_length=32)] = None
    animated: bool | None = None


class PollMediaCreateRequest(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=300)] = None
    emoji: PollEmojiCreateRequest = None


class PollAnswerCreateRequest(BaseModel):
    poll_media: PollMediaCreateRequest


class PollCreateRequest(BaseModel):
    question: PollMedia
    answers: Annotated[list[PollAnswerCreateRequest], Field(min_length=1, max_length=10)]
    allow_multiselect: bool | None = None
    layout_type: int | None = None
    duration: Annotated[int, Field(le=768, ge=1)] = None


class BaseCreateMessageCreateRequest(BaseModel):
    content: Annotated[str, Field(max_length=4000)] = None
    embeds: Annotated[list[RichEmbed], Field(max_length=10)] = None
    allowed_mentions: MessageAllowedMentionsRequest = None
    sticker_ids: Annotated[list[str], Field(max_length=3)] = None
    components: Annotated[list[str] | None, Field(max_length=40)] = None
    flags: int | None = None
    attachments: Annotated[list[MessageAttachmentRequest], Field(max_length=10)] = None
    poll: PollCreateRequest = None
    shared_client_theme: CustomClientThemeShareRequest = None
    confetti_potion: Dict[str, Any] = None


class CreateForumThreadRequest(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    auto_archive_duration: ThreadAutoArchiveDuration | None = None
    rate_limit_per_user: Annotated[int | None, Field(gt=0, le=21600)] = None
    applied_tags: Annotated[list[str] | None, Field(max_length=5, pattern=snowflake_pattern)] = None
    message: BaseCreateMessageCreateRequest


class ChannelTypes(Enum):
    ANNOUNCEMENT_THREAD = 10
    PUBLIC_THREAD = 11
    PRIVATE_THREAD = 12


class CreateTextThreadWithoutMessageRequest(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    auto_archive_duration: ThreadAutoArchiveDuration | None = None
    rate_limit_per_user: Annotated[int | None, Field(gt=0, le=21600)] = None
    applied_tags: Annotated[list[str] | None, Field(max_length=5, pattern=snowflake_pattern)] = None
    type: ChannelTypes
    invitable: bool | None = None


@mcp.tool()
async def create_thread(channel_id: Annotated[str, Field(pattern=snowflake_pattern)], create_thread_request: CreateForumThreadRequest | CreateTextThreadWithoutMessageRequest):
    thread = await api.create_thread(channel_id=channel_id, create_thread_request=CreateThreadRequest(create_thread_request))
    return thread

@mcp.tool()
async def list_guild_invites(guild_id: Annotated[str, Field(pattern=snowflake_pattern)]):
    invites = await api.list_guild_invites(guild_id=guild_id)
    return invites