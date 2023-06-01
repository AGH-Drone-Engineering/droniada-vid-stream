import asyncio
from grpc import aio
from droniada_vid_stream import video_streamer_pb2
from droniada_vid_stream import video_streamer_pb2_grpc
import cv2
import logging


class VideoStreamerServicer(video_streamer_pb2_grpc.VideoStreamerServicer):
    async def Stream(self, request: video_streamer_pb2.StreamRequest, context):
        cap = cv2.VideoCapture(request.cap)
        try:
            while True:
                ret, frame = cap.read()
                if ret:
                    scale = request.height / frame.shape[0]
                    frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
                    yield video_streamer_pb2.Image(data=cv2.imencode('.jpg', frame)[1].tobytes())
                else:
                    logging.warning('Camera read error')
        finally:
            cap.release()


async def serve():
    server = aio.server()
    video_streamer_pb2_grpc.add_VideoStreamerServicer_to_server(VideoStreamerServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
