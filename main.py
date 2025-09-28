# requirements: python-telegram-bot==20.7
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise SystemExit("Error: BOT_TOKEN environment variable not set.")

GRID_SIZE = 5

def recommend_strategy(amount: float):
    if amount < 50:
        mines = 3
    elif amount < 200:
        mines = 4
    elif amount < 500:
        mines = 6
    else:
        mines = 8

    corners = [(1,1),(1,GRID_SIZE),(GRID_SIZE,1),(GRID_SIZE,GRID_SIZE)]
    idx = int(amount) % 4
    first = corners[idx]
    clicks = [first]

    r,c = first
    if c+1 <= GRID_SIZE:
        clicks.append((r, c+1))
    else:
        clicks.append((r+1 if r+1<=GRID_SIZE else r, c-1 if c-1>=1 else c))

    r2,c2 = clicks[-1]
    third = (min(GRID_SIZE, r2+1), min(GRID_SIZE, c2+1))
    clicks.append(third)

    grid = [["🔵" for _ in range(GRID_SIZE)] for __ in range(GRID_SIZE)]
    for (rr,cc) in clicks:
        grid[rr-1][cc-1] = "⭐"
    ascii_grid = "\n".join("".join(row) for row in grid)
    return mines, clicks, ascii_grid

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalamualaikum 👋\nMain Mines Advisor Bot hoon.\n"
        "Mujhe sirf amount bhejo (jaise `48` ya `120`) aur main suggested mines count aur pehle 3 clicks bata dunga.\n"
        "Commands: /start /demo"
    )

async def demo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "DEMO / GUIDE:\n"
        "- Corner se start karo.\n- 1-2 safe clicks milen to cashout.\n- Main sirf guidance deta hoon; game random hota hai."
    )

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    token = text.split()[0].replace("PKR","").replace("rs","").replace("Rs","")
    try:
        amount = float(token)
    except:
        await update.message.reply_text("Amount samajh nahi aaya — sirf number bhejo (e.g. 48).")
        return

    mines, clicks, ascii_grid = recommend_strategy(amount)
    clicks_str = ", ".join([f"({r},{c})" for r,c in clicks])
    reply = (
        f"Bet: {int(amount)} PKR\n"
        f"Suggested mines (risk guide): {mines} mines\n"
        f"First 3 clicks (row,col): {clicks_str}\n\n"
        f"Grid (⭐ = suggested clicks):\n{ascii_grid}\n\n"
        "Note: Ye sirf guidance hai — game random hota hai. Responsible raho."
    )
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("demo", demo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_amount))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
