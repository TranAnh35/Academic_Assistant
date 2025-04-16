# Định nghĩa CoordinatorAgent

import logging
import dotenv
import os

dotenv.load_dotenv()

LOGS_DIR = os.getenv("LOGS_DIR", "log")
os.makedirs(LOGS_DIR, exist_ok=True)

# Xóa tất cả các handler mặc định trước khi cấu hình logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename=os.path.join(LOGS_DIR, "System.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode='w'  # Ghi đè file log mỗi lần chạy
)

from agents.sub_agent.search.agent import SearchAgent
from google.adk.agents import Agent

root_agent = Agent(
    name="Coordinator_Agent",
    model="gemini-2.0-flash",
    sub_agents=[SearchAgent],
)