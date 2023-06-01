import logging
import asyncio
from grpc import aio
import cv2
import numpy as np
from argparse import ArgumentParser

from droniada_vid_stream import video_streamer_pb2
from droniada_vid_stream import video_streamer_pb2_grpc


async def run():
    parser = ArgumentParser()
    parser.add_argument('--height', type=int, default=320)
    parser.add_argument('source', type=int)
    args = parser.parse_args()
    async with aio.insecure_channel('localhost:50051') as channel:
        stub = video_streamer_pb2_grpc.VideoStreamerStub(channel)
        async for response in stub.Stream(video_streamer_pb2.StreamRequest(cap=args.source, height=args.height)):
            frame = cv2.imdecode(np.frombuffer(response.data, np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow(f'Video Stream {args.source}', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
