# Start from busybox
FROM busybox:latest
# Copy the entry program into the image
COPY ./main.sh /main.sh
# Make it executable
RUN chmod +x /main.sh
# Make it run automatically when a container is created
ENTRYPOINT [ "/main.sh" ]
# Define default environment variables
ENV NAME=Your\ Name \
    SISTER=Your\ Sister \
    MUM=Your\ Mum \
    DAD=Your\ Dad
# Add some metadata
LABEL author="Simon Nganga"
LABEL author_email="theedushbag@gmail.com"
LABEL version="0.2"
