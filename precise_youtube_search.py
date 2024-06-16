import random
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

API_KEY = 'YOUR API KEY'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def display_ascii_art():
    ascii_art = """
█ ▄▄  █▄▄▄▄ ▄███▄   ▄█▄    ▄█    ▄▄▄▄▄   ▄███▄   
█   █ █  ▄▀ █▀   ▀  █▀ ▀▄  ██   █     ▀▄ █▀   ▀  
█▀▀▀  █▀▀▌  ██▄▄    █   ▀  ██ ▄  ▀▀▀▀▄   ██▄▄    
█     █  █  █▄   ▄▀ █▄  ▄▀ ▐█  ▀▄▄▄▄▀    █▄   ▄▀ 
 █      █   ▀███▀   ▀███▀   ▐            ▀███▀   
▀▄▀   ▄▀████▄   ▄     ▄▄▄▄▀ ▄   ███   ▄███▄      
  █  █  █   █    █ ▀▀▀ █     █  █  █  █▀   ▀     
   ▀█   █   █ █   █    █  █   █ █ ▀ ▄ ██▄▄       
   █    ▀████ █   █   █   █   █ █  ▄▀ █▄   ▄▀    
 ▄▀           █▄ ▄█  ▀    █▄ ▄█ ███   ▀███▀      
               ▀▀▀         ▀▀▀                   
   ▄▄▄▄▄   ▄███▄   ██   █▄▄▄▄ ▄█▄     ▄  █       
  █     ▀▄ █▀   ▀  █ █  █  ▄▀ █▀ ▀▄  █   █       
▄  ▀▀▀▀▄   ██▄▄    █▄▄█ █▀▀▌  █   ▀  ██▀▀█       
 ▀▄▄▄▄▀    █▄   ▄▀ █  █ █  █  █▄  ▄▀ █   █       
           ▀███▀      █   █   ▀███▀     █        
                     █   ▀             ▀         
                    ▀

    V1.0
    Made by astroyama with ChatGPT 3.5
    """
    print("\033[95m" + ascii_art + "\033[0m")

def get_random_video(keywords, date_type, year=None, exact_date=None):
    try:
        start_date, end_date = (
            (datetime(year, 1, 1), datetime(year, 12, 31, 23, 59, 59))
            if date_type == 'year'
            else (
                (exact_date_obj := datetime.strptime(exact_date, '%d/%m/%Y')),
                exact_date_obj.replace(hour=23, minute=59, second=59),
            )
        )

        search_response = youtube.search().list(
            part='id',
            type='video',
            order='date',
            maxResults=50,
            publishedAfter=start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            publishedBefore=end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            q=keywords,
        ).execute()

        videos = search_response.get('items', [])
        return f'https://www.youtube.com/watch?v={random.choice(videos)["id"]["videoId"]}' if videos else None

    except HttpError as e:
        print(f"An error occurred during the YouTube API call: {e}")
        return None

def save_links_to_file(file_path, num_links, keywords, date_type, year=None, exact_date=None):
    with open(file_path, 'w') as file:
        for _ in range(num_links):
            random_video_link = get_random_video(keywords, date_type, year, exact_date)
            if random_video_link:
                file.write(f'{random_video_link}\n')

if __name__ == '__main__':
    try:
        display_ascii_art()
        num_links = int(input('Enter the number of YouTube links to generate: '))
        keywords = input('Enter the keywords for the search (e.g., Touhou): ')
        date_type = input('Choose the date type (1. Year / 2. Exact date): ')
        year = int(input('Enter the year (e.g., 2008): ')) if date_type == '1' else None
        exact_date = input('Enter the exact date (in DD/MM/YYYY format): ') if date_type == '2' else None

    except ValueError:
        print('Please enter valid values.')
        exit()

    file_path = 'precise_youtube_search.txt'
    save_links_to_file(file_path, num_links, keywords, date_type, year, exact_date)
    print(f'{num_links} random YouTube links with keywords "{keywords}" saved to {file_path}')
