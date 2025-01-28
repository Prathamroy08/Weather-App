
import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime
from ttkthemes import ThemedTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("900x700")
        
        # Apply theme and styling
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Helvetica", 24, "bold"))
        self.style.configure("Info.TLabel", font=("Helvetica", 12))
        self.style.configure("Status.TLabel", font=("Helvetica", 10, "italic"))
        self.style.configure("Weather.TFrame", padding=15)
        
        # API configuration
        self.api_key = "21e6266283b1a0a2e4cd94ad6cd2468a"
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        # Create main container with padding
        self.main_frame = ttk.Frame(self.root, padding="20", style="Weather.TFrame")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Create UI elements
        self.create_ui()
        
        # Set default theme colors
        self.root.configure(bg="#f0f0f0")
        self.main_frame.configure(style="Weather.TFrame")
        
    def create_ui(self):
        # Title
        title_label = ttk.Label(
            self.main_frame, 
            text="Weather Dashboard", 
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Search frame with improved styling
        search_frame = ttk.Frame(self.main_frame)
        search_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        search_frame.columnconfigure(1, weight=1)
        
        # Search icon (using text as placeholder - you can replace with actual icon)
        search_icon = ttk.Label(search_frame, text="🔍", font=("Helvetica", 12))
        search_icon.grid(row=0, column=0, padx=(0, 5))
        
        # Enhanced city entry
        self.city_entry = ttk.Entry(
            search_frame, 
            width=40,
            font=("Helvetica", 12)
        )
        self.city_entry.grid(row=0, column=1, padx=5)
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        
        # Styled search button
        search_button = ttk.Button(
            search_frame,
            text="Get Weather",
            command=self.get_weather,
            style="Accent.TButton"
        )
        search_button.grid(row=0, column=2, padx=(5, 0))
        
        # Weather info display with cards
        self.info_frame = ttk.Frame(self.main_frame, padding="15")
        self.info_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        self.info_frame.columnconfigure(0, weight=1)
        
        # City information card
        self.city_card = ttk.LabelFrame(self.info_frame, padding="15")
        self.city_card.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        self.city_label = ttk.Label(
            self.city_card,
            text="",
            style="Title.TLabel"
        )
        self.city_label.pack(pady=5)
        
        # Main weather information card
        self.weather_card = ttk.LabelFrame(self.info_frame, padding="15")
        self.weather_card.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Create two columns for weather info
        left_frame = ttk.Frame(self.weather_card)
        left_frame.pack(side="left", expand=True, fill="both", padx=10)
        
        right_frame = ttk.Frame(self.weather_card)
        right_frame.pack(side="right", expand=True, fill="both", padx=10)
        
        # Left column weather information
        self.temp_label = ttk.Label(left_frame, text="", style="Info.TLabel")
        self.temp_label.pack(pady=5, anchor="w")
        
        self.feels_like_label = ttk.Label(left_frame, text="", style="Info.TLabel")
        self.feels_like_label.pack(pady=5, anchor="w")
        
        self.weather_desc_label = ttk.Label(left_frame, text="", style="Info.TLabel")
        self.weather_desc_label.pack(pady=5, anchor="w")
        
        # Right column weather information
        self.humidity_label = ttk.Label(right_frame, text="", style="Info.TLabel")
        self.humidity_label.pack(pady=5, anchor="w")
        
        self.pressure_label = ttk.Label(right_frame, text="", style="Info.TLabel")
        self.pressure_label.pack(pady=5, anchor="w")
        
        self.wind_label = ttk.Label(right_frame, text="", style="Info.TLabel")
        self.wind_label.pack(pady=5, anchor="w")
        
        # Footer with update information
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        self.last_updated_label = ttk.Label(
            footer_frame,
            text="",
            style="Status.TLabel"
        )
        self.last_updated_label.pack(side="left")
        
        self.status_label = ttk.Label(
            footer_frame,
            text="Ready to search",
            style="Status.TLabel"
        )
        self.status_label.pack(side="right")
    
    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name!")
            return
            
        try:
            self.status_label.config(text="Fetching weather data...")
            self.root.update()
            
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            weather_data = response.json()
            
            # Update UI with weather information
            self.city_label.config(
                text=f"{weather_data['name']}, {weather_data['sys']['country']}"
            )
            
            self.temp_label.config(
                text=f"🌡️ Temperature: {weather_data['main']['temp']}°C"
            )
            
            self.feels_like_label.config(
                text=f"🤔 Feels Like: {weather_data['main']['feels_like']}°C"
            )
            
            self.humidity_label.config(
                text=f"💧 Humidity: {weather_data['main']['humidity']}%"
            )
            
            self.pressure_label.config(
                text=f"📊 Pressure: {weather_data['main']['pressure']} hPa"
            )
            
            self.weather_desc_label.config(
                text=f"☁️ Weather: {weather_data['weather'][0]['description'].title()}"
            )
            
            self.wind_label.config(
                text=f"💨 Wind Speed: {weather_data['wind']['speed']} m/s"
            )
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.last_updated_label.config(
                text=f"Last Updated: {current_time}"
            )
            
            self.status_label.config(text="Weather data updated successfully")
            
        except requests.RequestException as e:
            self.status_label.config(text="Error: Failed to connect to weather service")
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
        except KeyError as e:
            self.status_label.config(text="Error: Invalid data received")
            messagebox.showerror("Error", "Failed to parse weather data")
        except Exception as e:
            self.status_label.config(text="Error: Unknown error occurred")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # You can choose different themes: 'arc', 'clearlooks', 'radiance', etc.
    app = WeatherApp(root)
    root.mainloop()
