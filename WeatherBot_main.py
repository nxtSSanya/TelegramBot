import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot  = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
	await message.reply("Tell me your city and I`ll talk to you current weather of it")

@dp.message_handler()
async def get_weather(message: types.Message):
	try:
		r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
		)
		data = r.json()

		city = data["name"]
		current_weather = data["main"]["temp"]
		humidity = data["main"]["humidity"]
		pressure = data["main"]["pressure"]
		wind_speed = data["wind"]["speed"]
		sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
		length_of_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		
		await message.reply(f"Current city is: {city}\nTemperature: {current_weather}C°\n"
              f"Humidity: {humidity}%\nPressure: {pressure} mm.rt.st\nWind speed: {wind_speed} mps\n"
              f"Sunrise at: {sunrise_time}\nSunset at: {sunset_time}\nLength of day: {length_of_day}\n"
              )
		#await message.reply("Current city is: " + city + "\nTemperature is: " + current_weather + "\nHumidity is: " + humidity + "\nPressure is: " + pressure + "\nWind speed is: " + wind_speed + "\nSunrise time is: " + sunrise_time + "\nSunset time is: " + sunset_time + "\nLength of day is: " + length_of_day)

	except Exception as ex:
		await message.reply("Wrong input data")

if __name__ == '__main__':
	executor.start_polling(dp)
