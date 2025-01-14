from __future__ import unicode_literals
from typing import *
from yt_dlp import YoutubeDL
from zeta_bot import (
    console,
    utils,
    audio
)

console = console.Console()

level = "YouTube模块"

async def get_info(ytb_url):

    ydl_opts = {
        'format': 'bestaudio/best',
        'extract_flat': True,
        "quiet": True,
    }

    await console.rp(f"开始提取信息：{ytb_url}", f"[{level}]")

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(ytb_url, download=False)

    video_id = info_dict["id"]
    video_title = info_dict["title"]

    await console.rp(f"信息提取完毕：{video_title} [{video_id}]", f"[{level}]")

    return info_dict


def get_filesize(info_dict: dict) -> Union[int, None]:
    if "filesize" in info_dict:
        return info_dict["filesize"]
    else:
        return None


async def audio_download(youtube_url, info_dict, download_path, download_type="youtube_single") -> audio.Audio:

    if download_path.endswith("/"):
        download_path = download_path.rstrip("/")

    video_id = info_dict["id"]
    video_title = info_dict["title"]
    video_path_title = utils.legal_name(video_title)
    video_name_extension = info_dict["ext"]
    video_duration = info_dict["duration"]
    size = utils.convert_byte(int(info_dict["filesize"]))

    video_path = f"{download_path}/{video_path_title}.{video_name_extension}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": video_path,
        "extract_flat": True,
        "quiet": True,
    }

    await console.rp(f"开始下载：{video_path_title}.{video_name_extension}", f"[{level}]")

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    new_audio = audio.Audio(video_title, download_type, video_id, video_path, video_duration)
    await console.rp(
        f"下载完成\n"
        f"文件名：{video_path_title}.{video_name_extension}\n"
        f"来源：[YouTube] {video_id}\n"
        f"路径：{download_path}\n"
        f"大小：{size[0]} {size[1]}\n"
        f"时长：{utils.convert_duration_to_str(video_duration)}",
        f"[{level}]"
    )

    return new_audio


async def search(query, query_num=5) -> list:

    query = query.strip()

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': "./downloads/" + '/%(title)s.%(ext)s',
        'default_search': "ytsearch",
        'extract_flat': True,
        "quiet": True,
    }

    if query == "":
        return []

    await console.rp(f"开始搜索：{query}", f"[{level}]")

    with YoutubeDL(ydl_opts) as ydl:
        extracted_info = ydl.extract_info(f"ytsearch{query_num}:{query}", download=False)

    result = []
    log_message = f"搜索 {query} 结果为："
    counter = 1

    id_header = "https://www.youtube.com/watch?v="

    for item in extracted_info["entries"]:
        if counter > query_num:
            break
        result.append(
            {
                "title": item["title"],
                "id": id_header + item["id"],
                "duration": item["duration"],
                "duration_str": utils.convert_duration_to_str(item["duration"]),
            }
        )
        log_message += f"\n{counter}. {item['id']}：{item['title']} [{utils.convert_duration_to_str(item['duration'])}]"
        counter += 1

    await console.rp(log_message, f"[{level}]")

    return result
