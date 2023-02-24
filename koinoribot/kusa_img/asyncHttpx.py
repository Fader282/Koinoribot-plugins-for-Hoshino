from typing import Dict, Union, Optional, List, Any
from retrying import retry
from httpx import Response, ConnectTimeout
from .useragent import get_user_agent
import httpx
from pathlib import Path
import hoshino
import aiofiles
import asyncio



class AsyncHttpx:

    proxy = {"http://127.0.0.1:7890", "https://127.0.0.1:7890"}

    @classmethod
    @retry(stop_max_attempt_number=3)
    async def get(
        cls,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> Response:
        """
        说明：
            Get
        参数：
            :param url: url
            :param params: params
            :param headers: 请求头
            :param cookies: cookies
            :param use_proxy: 使用默认代理
            :param proxy: 指定代理
            :param timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            return await client.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                **kwargs
            )

    @classmethod
    async def post(
        cls,
        url: str,
        *,
        data: Optional[Dict[str, str]] = None,
        content: Any = None,
        files: Any = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        json: Optional[Dict[str, Union[Any]]] = None,
        params: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> Response:
        """
        说明：
            Post
        参数：
            :param url: url
            :param data: data
            :param content: content
            :param files: files
            :param use_proxy: 是否默认代理
            :param proxy: 指定代理
            :param json: json
            :param params: params
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
        """
        if not headers:
            headers = get_user_agent()
        proxy = proxy if proxy else cls.proxy if use_proxy else None
        async with httpx.AsyncClient(proxies=proxy) as client:
            return await client.post(
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
                **kwargs,
            )

    @classmethod
    async def download_file(
        cls,
        url: str,
        path: Union[str, Path],
        *,
        params: Optional[Dict[str, str]] = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> bool:
        """
        说明：
            下载文件
        参数：
            :param url: url
            :param path: 存储路径
            :param params: params
            :param use_proxy: 使用代理
            :param proxy: 指定代理
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
        """
        if isinstance(path, str):
            path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            for _ in range(3):
                try:
                    content = (
                        await cls.get(
                            url,
                            params=params,
                            headers=headers,
                            cookies=cookies,
                            use_proxy=use_proxy,
                            proxy=proxy,
                            timeout=timeout,
                            **kwargs,
                        )
                    ).content
                    async with aiofiles.open(path, "wb") as wf:
                        await wf.write(content)
                        hoshino.logger.info(f"下载 {url} 成功.. Path：{path.absolute()}")
                    return True
                except (TimeoutError, ConnectTimeout):
                    pass
            else:
                hoshino.logger.error(f"下载 {url} 下载超时.. Path：{path.absolute()}")
        except Exception as e:
            hoshino.logger.error(f"下载 {url} 未知错误 {type(e)}：{e}.. Path：{path.absolute()}")
        return False

    @classmethod
    async def gather_download_file(
        cls,
        url_list: List[str],
        path_list: List[Union[str, Path]],
        *,
        limit_async_number: Optional[int] = None,
        params: Optional[Dict[str, str]] = None,
        use_proxy: bool = True,
        proxy: Dict[str, str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        timeout: Optional[int] = 30,
        **kwargs,
    ) -> List[bool]:
        """
        说明：
            分组同时下载文件
        参数：
            :param url_list: url列表
            :param path_list: 存储路径列表
            :param limit_async_number: 限制同时请求数量
            :param params: params
            :param use_proxy: 使用代理
            :param proxy: 指定代理
            :param headers: 请求头
            :param cookies: cookies
            :param timeout: 超时时间
        """
        if n := len(url_list) != len(path_list):
            raise UrlPathNumberNotEqual(
                f"Url数量与Path数量不对等，Url：{len(url_list)}，Path：{len(path_list)}"
            )
        if limit_async_number and n > limit_async_number:
            m = float(n) / limit_async_number
            x = 0
            j = limit_async_number
            _split_url_list = []
            _split_path_list = []
            for _ in range(int(m)):
                _split_url_list.append(url_list[x:j])
                _split_path_list.append(path_list[x:j])
                x += limit_async_number
                j += limit_async_number
            if int(m) < m:
                _split_url_list.append(url_list[j:])
                _split_path_list.append(path_list[j:])
        else:
            _split_url_list = [url_list]
            _split_path_list = [path_list]
        tasks = []
        result_ = []
        for x, y in zip(_split_url_list, _split_path_list):
            for url, path in zip(x, y):
                tasks.append(
                    asyncio.create_task(
                        cls.download_file(
                            url,
                            path,
                            params=params,
                            headers=headers,
                            cookies=cookies,
                            use_proxy=use_proxy,
                            timeout=timeout,
                            proxy=proxy,
                            ** kwargs,
                        )
                    )
                )
            _x = await asyncio.gather(*tasks)
            result_ = result_ + list(_x)
            tasks.clear()
        return result_


class UrlPathNumberNotEqual(Exception):
    pass
