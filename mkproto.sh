#!/usr/bin/env sh

python -m grpc_tools.protoc -Iprotos --python_out=droniada_vid_stream --pyi_out=droniada_vid_stream --grpc_python_out=droniada_vid_stream protos/video_streamer.proto
