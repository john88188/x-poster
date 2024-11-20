import os
import json
import random
import schedule
import time
from datetime import datetime
import pytz
import tweepy
from dotenv import load_dotenv
from pathlib import Path
import logging
from pythonjsonlogger import jsonlogger

# 配置日志
def setup_logger():
    logger = logging.getLogger('twitter_bot')
    logHandler = logging.FileHandler('bot.log')
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

# 加载环境变量
load_dotenv()

class TwitterBot:
    def __init__(self):
        self.settings = self._load_settings()
        self.posted_history = self._load_history()
        self.client = self._setup_twitter_client()
        
    def _load_settings(self):
        with open('settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_history(self):
        history_file = self.settings['files']['history_file']
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"posted_files": []}

    def _save_history(self):
        with open(self.settings['files']['history_file'], 'w', encoding='utf-8') as f:
            json.dump(self.posted_history, f, indent=4)

    def _setup_twitter_client(self):
        auth = tweepy.OAuthHandler(
            os.getenv('TWITTER_API_KEY'),
            os.getenv('TWITTER_API_SECRET')
        )
        auth.set_access_token(
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )
        return tweepy.API(auth)

    def get_random_content(self):
        content_dir = Path(self.settings['files']['content_dir'])
        if not content_dir.exists():
            content_dir.mkdir(parents=True)
            logger.error(f"Content directory {content_dir} did not exist and was created")
            return None

        md_files = list(content_dir.glob('*.md'))
        unposted_files = [f for f in md_files if str(f) not in self.posted_history['posted_files']]

        if not unposted_files:
            logger.warning("No unposted files available")
            return None

        selected_file = random.choice(unposted_files)
        try:
            with open(selected_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            return {
                'file_path': str(selected_file),
                'content': content
            }
        except Exception as e:
            logger.error(f"Error reading file {selected_file}: {str(e)}")
            return None

    def format_content(self, content):
        max_length = self.settings['content']['max_length']
        hashtags = ' '.join(self.settings['content']['hashtags'])
        
        # 如果设置了添加时间戳
        timestamp = ''
        if self.settings['content']['add_timestamp']:
            timestamp = f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"

        # 计算实际可用的内容长度
        available_length = max_length - len(hashtags) - len(timestamp) - 2

        # 如果内容太长，进行截断
        if len(content) > available_length:
            content = content[:available_length-3] + "..."

        return f"{content}{timestamp}\n{hashtags}"

    def post_tweet(self):
        content_data = self.get_random_content()
        if not content_data:
            return

        formatted_content = self.format_content(content_data['content'])
        
        try:
            self.client.update_status(formatted_content)
            self.posted_history['posted_files'].append(content_data['file_path'])
            self._save_history()
            logger.info(f"Successfully posted content from {content_data['file_path']}")
        except Exception as e:
            logger.error(f"Error posting tweet: {str(e)}")

def run_bot():
    try:
        bot = TwitterBot()
        bot.post_tweet()
    except Exception as e:
        logger.error(f"Bot execution error: {str(e)}")

def schedule_jobs():
    settings = json.load(open('settings.json', 'r', encoding='utf-8'))
    schedule_settings = settings['schedule']
    
    # 设置时区
    timezone = pytz.timezone(schedule_settings['timezone'])
    
    # 设置定时任务
    schedule.every(schedule_settings['interval_minutes']).minutes.do(run_bot)

if __name__ == "__main__":
    logger.info("Bot started")
    schedule_jobs()
    
    while True:
        schedule.run_pending()
        time.sleep(60)
