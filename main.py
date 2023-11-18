import os
from pytube import YouTube
from tqdm import tqdm
import requests

def sanitize_filename(filename):
    invalid_chars = {'/', '\\', '?', '%', '*', ':', '|', '"', '<', '>', '.'}
    return ''.join(char if char not in invalid_chars else '_' for char in filename)

def download_with_progress_bar(url, output_path='.', resolution='highest'):
    try:
        # Create a YouTube object
        yt = YouTube(url)

        # Get the video streams
        video_streams = yt.streams

        # Filter streams based on resolution
        if resolution.lower() == 'highest':
            video_stream = video_streams.get_highest_resolution()
        else:
            video_stream = video_streams.filter(res=resolution).first()

        # Get the video title for naming the file
        video_title = yt.title

        # Sanitize the video title for file naming
        video_title = sanitize_filename(video_title)

        # Set the output path for the downloaded file
        output_file_path = os.path.join(output_path, f'{video_title}.mp4')

        # Get the video stream URL
        video_url = video_stream.url

        # Make a request to the video stream URL
        response = requests.get(video_url, stream=True)

        # Get the total file size from the response headers
        total_size = int(response.headers.get('content-length', 0))

        # Download the video with progress bar
        print(f'Downloading: {video_title} ({video_stream.resolution})')
        with open(output_file_path, 'wb') as f, tqdm(
                desc=video_title,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                bar.update(len(data))
                f.write(data)

        print(f'Download complete! Saved as: {output_file_path}')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    video_url = input("Enter YouTube video URL: ")
    resolution = input("Enter desired resolution (or 'highest'): ")
    output_path = input("Enter the output path (press Enter for the current directory): ") or '.'
    
    download_with_progress_bar(video_url, output_path, resolution)