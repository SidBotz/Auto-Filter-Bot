import os, string, logging, random, asyncio, time, datetime, re, sys, json, base64
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import *
from database.users_chats_db import db, delete_all_referal_users, get_referal_users_count, get_referal_all_users, referal_add_user
from info import CLONE_MODE, OWNER_LNK, REACTIONS, CHANNELS, REQUEST_TO_JOIN_MODE, TRY_AGAIN_BTN, ADMINS, SHORTLINK_MODE, PREMIUM_AND_REFERAL_MODE, STREAM_MODE, AUTH_CHANNEL, REFERAL_PREMEIUM_TIME, REFERAL_COUNT, PAYMENT_TEXT, PAYMENT_QR, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, PROTECT_CONTENT, CHNL_LNK, GRP_LNK, REQST_CHANNEL, SUPPORT_CHAT_ID, SUPPORT_CHAT, MAX_B_TN, VERIFY, SHORTLINK_API, SHORTLINK_URL, TUTORIAL, VERIFY_TUTORIAL, IS_TUTORIAL, URL
from utils import get_settings, pub_is_subscribed, get_size, is_subscribed, save_group_settings, temp, verify_user, check_token, check_verification, get_token, get_shortlink, get_tutorial, get_seconds
from database.connections_mdb import active_connection
from urllib.parse import quote_plus
logger = logging.getLogger(__name__)
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Constants for verification
VERIFY = True  # Toggle verification requirement
VERIFY_TUTORIAL = "https://example.com/verify-tutorial"  # Replace with your tutorial link
CONTACT_ADMIN = "https://t.me/AdminUsername"  # Replace with your admin's Telegram link




# Start command handler
@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    try:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    except:
        pass
    args = message.text.split(" ", 1)
    if len(args) == 1:
        # User has not provided additional arguments
        if VERIFY and not await check_verification(client, message.from_user.id):
            verify_url = await get_token(client, message.from_user.id, f"https://telegram.me/{client.me.username}?start=")
            btn = [
                [InlineKeyboardButton("Verify", url=verify_url)],
                [InlineKeyboardButton("How To Open Link & Verify", url=VERIFY_TUTORIAL)],
                [InlineKeyboardButton("Contact Admin", url=CONTACT_ADMIN)]
            ]
            await message.reply_text(
                text="<b>You are not verified!\nKindly verify to continue or contact admin for assistance!</b>",
                protect_content=True,
                reply_markup=InlineKeyboardMarkup(btn)
            )
        elif await check_verification(client, message.from_user.id):
            await message.reply_text(
                text="<b>Welcome! You are already verified. Enjoy our services!</b>",
                protect_content=True
            )
        else:
            btn = [[InlineKeyboardButton("Contact Admin", url=CONTACT_ADMIN)]]
            await message.reply_text(
                text="<b>Unable to determine your verification status.\nPlease contact the admin for assistance!</b>",
                protect_content=True,
                reply_markup=InlineKeyboardMarkup(btn)
            )
    elif len(args) > 1:
        # User has provided additional arguments
        data = args[1]
        if data.split("-", 1)[0] == "verify":
            userid = data.split("-", 2)[1]
            token = data.split("-", 3)[2]
            if str(message.from_user.id) != str(userid):
                return await message.reply_text(
                    text="<b>Invalid link or Expired link!</b>",
                    protect_content=True
                )
            is_valid = await check_token(client, userid, token)
            if is_valid:
                await message.reply_text(
                    text=f"<b>Hey {message.from_user.mention}, You are successfully verified!\n"
                         f"Now you have unlimited access for all movies till today midnight.</b>",
                    protect_content=True
                )
                await verify_user(client, userid, token)
            else:
                await message.reply_text(
                    text="<b>Invalid link or Expired link!</b>",
                    protect_content=True
                )
