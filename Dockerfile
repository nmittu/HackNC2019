from python:3.7

RUN pip install opencv-python scipy Pillow pyserial

COPY color_reader.py .
COPY img-colors.pkl .

ENTRYPOINT python color_reader.py