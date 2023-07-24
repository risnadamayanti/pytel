# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# Please read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from os import remove
from pyrogram.enums import ChatType
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.forbidden_403 import (
    ChatSendMediaForbidden,)
from . import (
    _try_purged,
    eor,
    get_text,
    is_url,
    plugins_helper,
    px,
    pytel,
    suppress,
    random_prefixies,)


@pytel.instruction(
    ["swipper"],
    outgoing=True,
)
async def _swipper(client, message):
    url = get_text(
        message, save_link=True
    )
    if not url or not (
        is_url(url) is True
    ):
        await eor(
            message,
            text="Provide a valid link telegram!",
        )
    x = await eor(
        message,
        text="Swipper...",
    )
    if url.startswith("https"):
        if "?single" in url:
            link_ = url.split(
                "?single"
            )[0]
            msg_id = int(
                link_.split("/")[-1]
            )
        else:
            msg_id = int(
                url.split("/")[-1]
            )
        if "t.me/c/" in url:
            try:
                chat = int(
                    "-100"
                    + str(
                        url.split("/")[
                            -2
                        ]
                    )
                )
                m = await client.get_messages(
                    chat, msg_id
                )
            except RPCError:
                await eor(
                    x,
                    text="#RPCError Something problems...",
                )
                return
            try:
                await client.copy_message(
                    message.chat.id,
                    chat,
                    msg_id,
                    reply_to_message_id=message.id,
                )
                await _try_purged(
                    x, 1.5
                )
            except Exception:
                await downloads_media(
                    client, message, m
                )
            await _try_purged(x, 1.5)
            return
        else:
            try:
                chat = str(
                    url.split("/")[-2]
                )
                ms = await client.get_chat(
                    chat
                )
            except RPCError:
                await eor(
                    x,
                    text="#RPCError Something problems...",
                )
            if (
                ms.type
                == ChatType.CHANNEL
            ):
                m = await client.get_messages(
                    chat, msg_id
                )
                await downloads_media(
                    client, message, m
                )
                await _try_purged(
                    x, 1.5
                )
                return
            else:
                try:
                    await client.copy_message(
                        message.chat.id,
                        chat,
                        msg_id,
                        reply_to_message_id=message.id,
                    )
                    await _try_purged(
                        x, 1.5
                    )
                except Exception:
                    m = await client.get_messages(
                        chat, msg_id
                    )
                    await downloads_media(
                        client,
                        message,
                        m,
                    )
                    await _try_purged(
                        x, 1.5
                    )
                    return


async def downloads_media(
    client, message, m
):
    caption = (
        m.caption
        or m.caption_entities
        or None
    )
    with suppress(
        ChatSendMediaForbidden
    ):
        if (m.text) or (m.sticker):
            await m.copy(
                message.chat.id,
                reply_to_message_id=message.id,
            )
        if m.photo:
            photo = await client.download_media(
                m.photo
            )
            await client.send_document(
                message.chat.id,
                document=photo,
                caption=caption,
                force_document=True,
                reply_to_message_id=message.id,
            )
            remove(photo)
        if m.video:
            video = await client.download_media(
                m.video
            )
            await client.send_document(
                message.chat.id,
                document=video,
                caption=caption,
                force_document=True,
                reply_to_message_id=message.id,
            )
            remove(video)
        if m.document:
            file = await client.download_media(
                m.document
            )
            await client.send_document(
                message.chat.id,
                document=file,
                caption=caption,
                force_document=True,
                reply_to_message_id=message.id,
            )
            remove(file)
        if m.audio:
            audio = await client.download_media(
                m.audio
            )
            await client.send_audio(
                message.chat.id,
                audio,
                caption,
                reply_to_message_id=message.id,
            )
            remove(audio)
        if m.voice:
            voice = await client.download_media(
                m.voice
            )
            await client.send_voice(
                message.chat.id,
                voice,
                caption,
                reply_to_message_id=message.id,
            )
            remove(voice)
        if m.animation:
            animation = await client.download_media(
                m.animation
            )
            await client.send_animation(
                message.chat.id,
                animation,
                caption,
                reply_to_message_id=message.id,
            )
            remove(animation)


plugins_helper["swipper"] = {
    f"{random_prefixies(px)}swipper [link messages media channel]": "To swipper media private in channels.",
}
