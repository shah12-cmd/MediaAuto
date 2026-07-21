"""Telegram bot handlers for management interface"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


class BotHandlers:
    """Handle Telegram bot interactions"""
    
    def __init__(self, config_manager, db_manager):
        self.config_manager = config_manager
        self.db_manager = db_manager
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user_id = update.effective_user.id
        
        keyboard = [
            [InlineKeyboardButton("📥 مدیریت کانال‌های مبدا", callback_data="manage_sources")],
            [InlineKeyboardButton("📤 تنظیم کانال مقصد", callback_data="set_destination")],
            [InlineKeyboardButton("⏰ تنظیم زمان ارسال", callback_data="set_delay")],
            [InlineKeyboardButton("📝 تنظیم متن تبلیغاتی", callback_data="set_ad_text")],
            [InlineKeyboardButton("✏️ تنظیم ویرایش کپشن", callback_data="caption_settings")],
            [InlineKeyboardButton("🤖 تنظیم هوش مصنوعی", callback_data="ai_settings")],
            [InlineKeyboardButton("🖼 تنظیم واترمارک", callback_data="watermark_settings")],
            [InlineKeyboardButton("📊 آمار ربات", callback_data="statistics")],
            [InlineKeyboardButton("📜 مشاهده لاگ‌ها", callback_data="view_logs")],
            [InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings")],
            [InlineKeyboardButton("🔄 ری‌استارت ربات", callback_data="restart_bot")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👋 خوش آمدید به MediaAuto Bot!\n\n"
            "لطفا یک گزینه را انتخاب کنید:",
            reply_markup=reply_markup
        )
    
    async def manage_sources_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Manage source channels"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("➕ افزودن کانال", callback_data="add_source")],
            [InlineKeyboardButton("❌ حذف کانال", callback_data="remove_source")],
            [InlineKeyboardButton("📋 لیست کانال‌ها", callback_data="list_sources")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📥 مدیریت کانال‌های مبدا\n\n"
            "لطفا یک گزینه را انتخاب کنید:",
            reply_markup=reply_markup
        )
    
    async def add_source_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Add source channel"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "📥 افزودن کانال مبدا\n\n"
            "لطفا شناسه کانال را وارد کنید:\n"
            "مثال: @channelname یا 123456789"
        )
        
        context.user_data['action'] = 'add_source'
    
    async def set_destination_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Set destination channel"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "📤 تنظیم کانال مقصد\n\n"
            "لطفا شناسه کانال مقصد را وارد کنید:\n"
            "مثال: @destination_channel یا 123456789"
        )
        
        context.user_data['action'] = 'set_destination'
    
    async def set_delay_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Set send delay"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("⏱ 5 دقیقه", callback_data="delay_300")],
            [InlineKeyboardButton("⏱ 10 دقیقه", callback_data="delay_600")],
            [InlineKeyboardButton("⏱ 30 دقیقه", callback_data="delay_1800")],
            [InlineKeyboardButton("⏱ 1 ساعت", callback_data="delay_3600")],
            [InlineKeyboardButton("⏱ دلخواه", callback_data="delay_custom")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "⏰ تنظیم زمان ارسال\n\n"
            "لطفا زمان ارسال را انتخاب کنید:",
            reply_markup=reply_markup
        )
    
    async def set_ad_text_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Set advertisement text"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            "📝 تنظیم متن تبلیغاتی\n\n"
            "لطفا متن تبلیغاتی را وارد کنید:\n"
            "(برای حذف، خط خالی بفرستید)"
        )
        
        context.user_data['action'] = 'set_ad_text'
    
    async def caption_settings_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Caption editing settings"""
        query = update.callback_query
        await query.answer()
        
        config = self.config_manager.config
        
        keyboard = [
            [InlineKeyboardButton(
                "🔗 حذف لینک‌های کانال: " + ("✅" if config.remove_channel_links else "❌"),
                callback_data="toggle_remove_links"
            )],
            [InlineKeyboardButton(
                "🔢 حذف آیدی‌های کانال: " + ("✅" if config.remove_channel_ids else "❌"),
                callback_data="toggle_remove_ids"
            )],
            [InlineKeyboardButton(
                "🗑 حذف تبلیغات: " + ("✅" if config.remove_ads else "❌"),
                callback_data="toggle_remove_ads"
            )],
            [InlineKeyboardButton(
                "#️⃣ حذف هشتگ‌های اضافی: " + ("✅" if config.remove_extra_hashtags else "❌"),
                callback_data="toggle_remove_hashtags"
            )],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "✏️ تنظیم ویرایش کپشن\n\n"
            "لطفا تنظیمات را انتخاب کنید:",
            reply_markup=reply_markup
        )
    
    async def ai_settings_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """AI settings"""
        query = update.callback_query
        await query.answer()
        
        config = self.config_manager.config
        
        keyboard = [
            [InlineKeyboardButton(
                "فعال: " + ("✅" if config.ai_enabled else "❌"),
                callback_data="toggle_ai"
            )],
            [InlineKeyboardButton("🔑 API Key", callback_data="set_ai_key")],
            [InlineKeyboardButton("🎯 بازنویسی کپشن", callback_data="ai_rewrite")],
            [InlineKeyboardButton("✂️ کوتاه کردن", callback_data="ai_shorten")],
            [InlineKeyboardButton("✨ جذاب کردن", callback_data="ai_attractive")],
            [InlineKeyboardButton("😊 اضافه کردن ایموجی", callback_data="ai_emoji")],
            [InlineKeyboardButton("🇮🇷 ترجمه فارسی", callback_data="ai_translate")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🤖 تنظیم هوش مصنوعی\n\n"
            "لطفا گزینه‌ای را انتخاب کنید:",
            reply_markup=reply_markup
        )
    
    async def watermark_settings_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Watermark settings"""
        query = update.callback_query
        await query.answer()
        
        config = self.config_manager.config
        
        keyboard = [
            [InlineKeyboardButton(
                "فعال: " + ("✅" if config.watermark_enabled else "❌"),
                callback_data="toggle_watermark"
            )],
            [InlineKeyboardButton("📝 متن واترمارک", callback_data="set_watermark_text")],
            [InlineKeyboardButton("🖼 تصویر واترمارک", callback_data="set_watermark_image")],
            [InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🖼 تنظیم واترمارک\n\n"
            "لطفا گزینه‌ای را انتخاب کنید:",
            reply_markup=reply_markup
        )
    
    async def statistics_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show statistics"""
        query = update.callback_query
        await query.answer()
        
        stats = self.db_manager.get_statistics()
        
        text = (
            f"📊 آمار ربات\n\n"
            f"📨 کل پیام‌های ارسال شده: {stats.get('total_messages', 0)}\n"
            f"📺 کل کانال‌ها: {stats.get('total_channels', 0)}\n"
            f"✅ کانال‌های فعال: {stats.get('active_channels', 0)}\n"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def view_logs_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """View bot logs"""
        query = update.callback_query
        await query.answer()
        
        logs = self.db_manager.get_logs(limit=20)
        
        logs_text = "📜 لاگ‌های ربات (آخرین 20)\n\n"
        for log in logs:
            logs_text += f"[{log.level}] {log.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n{log.message}\n\n"
        
        if not logs:
            logs_text += "هیچ لاگی موجود نیست."
        
        keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(logs_text, reply_markup=reply_markup)
    
    async def restart_bot_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Restart bot"""
        query = update.callback_query
        await query.answer()
        
        keyboard = [
            [InlineKeyboardButton("✅ تایید", callback_data="confirm_restart")],
            [InlineKeyboardButton("❌ لغو", callback_data="main_menu")],
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔄 آیا مطمئن هستید که می‌خواهید ربات را دوباره راه‌اندازی کنید؟",
            reply_markup=reply_markup
        )
