from typing import Any, Optional, Tuple

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from config import I18N_DOMAIN, LOCALES_DIR
from database.db import DBCommands

# ================ DATA BASE SETTINGS =================================================================================


db = DBCommands()


# =====================================================================================================================


async def get_lang(user_id):
    user = await db.get_user(user_id)
    if user:
        return user.language


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = types.User.get_current()
        return await get_lang(user.id) or user.locale

    async def trigger(self, action, args):
        """
        Custom Event trigger

        :param action: event name
        :param args: event arguments
        :return:
        """
        if (
            "update" not in action
            and "error" not in action
            and (action.startswith("pre_process") or action == "set_language")
        ):
            locale = await self.get_user_locale(action, args)
            self.ctx_locale.set(locale)
            return True


def setup_middleware(dp):
    i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n
