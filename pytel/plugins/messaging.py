# pytel < https://t.me/kastaid >
# Copyright (C) 2023-present kastaid
#
# This file is a part of < https://github.com/kastaid/pytel/ >
# PLease read the GNU Affero General Public License in
# < https://github.com/kastaid/pytel/blob/main/LICENSE/ >

from asyncio import sleep
from datetime import datetime, timedelta
from typing import Optional
from . import (
    _try_purged,
    plugins_helper,
    px,
    pytel,
    random_prefixies,
    eor,
    tz,
    suppress,
    ParseMode,)

_SCHEDULE: list = []
_DSPAM: list = []

schedule_example = f"""
--**Command Guide**-- ›_

__Schedule Messages__

**Run ›_**
`{random_prefixies(px)}schmsg [time in seconds: schedule] [number of messages] [time sleep in seconds] [messages: support html]`

**Examples:**
`{random_prefixies(px)}schmsg 240 5 360 Hello`

```
240    5     360   Hello
 |     |      |      |
time, count, time, message
```
**Time Example:**
`240 = 4 minute`
__1 minute equals 60 seconds__

**Message Example (HTML):**
<spoiler>Hello World</spoiler>

**HTML Support:**
<spoiler> text </spoiler>
<a href='url'> Hello World </a>
<b> Text </b>
<i> Text </i>
<u> Text </u>
<url> URL </url>
<code> Text </code>
<pre> Text </pre>
<strong> Text </strong>
"""


@pytel.instruction(
    ["del", "delete"],
    outgoing=True,
)
async def _delete(client, message):
    replieds = message.reply_to_message
    if replieds:
        await _try_purged(replieds)
        await _try_purged(
            message,
            0.9,
        )
        return
    else:
        await _try_purged(
            message,
            0.4,
        )


@pytel.instruction(
    ["purgeme"],
    outgoing=True,
)
async def _purge_me(client, message):
    if len(message.command) != 2:
        return await message.delete()

    user_id = client.me.id
    n = message.text.split(None, 1)[
        1
    ].strip()
    if not n.isnumeric():
        return await eor(
            message,
            text="Invalid Args",
        )

    n = int(n)
    if n < 1:
        n: int = 2

    chat_id = message.chat.id
    message_ids = [
        m.id
        async for m in client.search_messages(
            chat_id,
            from_user=int(user_id),
            limit=n,
        )
    ]

    if not message_ids:
        return await eor(
            message,
            text="No messages found.",
        )

    to_delete = [
        message_ids[i : i + 99]
        for i in range(
            0,
            len(message_ids),
            99,
        )
    ]
    for (
        hundred_messages_or_less
    ) in to_delete:
        await client.delete_messages(
            chat_id=chat_id,
            message_ids=hundred_messages_or_less,
            revoke=True,
        )


@pytel.instruction(
    ["schedule"],
    outgoing=True,
)
async def _schedule_msg(
    client, message
):
    chat_id: Optional[
        int
    ] = message.chat.id
    if chat_id in list(_SCHEDULE):
        await eor(
            message,
            text="Please wait until previous --schedule-- msg are finished..",
        )
        return
    try:
        args = message.text.split(
            None, 4
        )
        schtimes = float(args[1])
        count = int(args[2])
        tms = float(args[3])
        mesg = str(args[4])
    except BaseException:
        await eor(
            message,
            text=schedule_example,
            parse_mode=ParseMode.MARKDOWN,
        )
        return
    await message.delete()
    with suppress(BaseException):
        _SCHEDULE.append(chat_id)
        schtimes = (
            60
            if schtimes
            and schtimes < 60
            else schtimes
        )
        timesleep = (
            60
            if tms and tms < 60
            else tms
        )
        for _ in range(count):
            if chat_id not in list(
                _SCHEDULE
            ):
                break
            else:
                t = datetime.now(
                    tz
                ) + timedelta(
                    seconds=schtimes
                )
                await client.send_message(
                    int(chat_id),
                    text=mesg,
                    parse_mode=ParseMode.HTML,
                    schedule_date=t,
                )
                await sleep(timesleep)


@pytel.instruction(
    ["dsp"],
    outgoing=True,
)
async def _dspam_msg(client, message):
    chat_id: Optional[
        int
    ] = message.chat.id
    if chat_id in list(_DSPAM):
        await eor(
            message,
            text="Please wait until previous --delay spam-- are finished..",
        )
        return
    try:
        args = message.text.split(
            None, 3
        )
        count = int(args[2])
        tms = float(args[1])
        mesg = str(args[3])
    except BaseException:
        await eor(
            message,
            text=f"{random_prefixies(px)}dsp [seconds] [count] [text]",
        )
        return
    timesleep = (
        60 if tms and tms < 60 else tms
    )
    await message.delete()
    with suppress(BaseException):
        for _ in range(count):
            if chat_id not in list(
                _DSPAM
            ):
                break
            else:
                await client.send_message(
                    int(chat_id),
                    text=mesg,
                    parse_mode=ParseMode.HTML,
                )
                await sleep(timesleep)


@pytel.instruction(
    ["schcancel"],
    outgoing=True,
)
async def _cancel_schedule_msg(
    client, message
):
    chat_id: Optional[
        int
    ] = message.chat.id
    x = await eor(
        message,
        text="Canceling schedule messages...",
    )
    if chat_id not in list(_SCHEDULE):
        await eor(
            x,
            text="No current --**Schedule**-- msg are running or cancel in --schedule-- msg.",
        )
        return
    _SCHEDULE.remove(chat_id)
    await eor(
        x,
        text="--**Schedule**-- messages has been canceled.",
    )


@pytel.instruction(
    ["dspcancel"],
    outgoing=True,
)
async def _cancel_dspam_msg(
    client, message
):
    chat_id: Optional[
        int
    ] = message.chat.id
    x = await eor(
        message,
        text="Canceling delay-spam messages...",
    )
    if chat_id not in list(_DSPAM):
        await eor(
            x,
            text="No current --**DSpam**-- msg are running.",
        )
        return
    _DSPAM.remove(chat_id)
    await eor(
        x,
        text="--**DSpam**-- messages has been canceled.",
    )


plugins_helper["messaging"] = {
    f"{random_prefixies(px)}del [reply message]": "To deleted ur messages.",
    f"{random_prefixies(px)}purgeme [count]": "To purged ur messages.",
    f"{random_prefixies(px)}schedule [seconds] [count] [seconds] [text]": "To send schedule message.",
    f"{random_prefixies(px)}schcancel": "To cancel ur schedule message.",
    f"{random_prefixies(px)}dsp [seconds] [count] [text]": "To send delay-spam message.",
    f"{random_prefixies(px)}dspcancel": "To cancel ur delay-spam message.",
}
