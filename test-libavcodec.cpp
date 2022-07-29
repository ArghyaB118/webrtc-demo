// http://www.ffmpeg.org/doxygen/trunk/dir_687bdf86e8e626c2168c3a2d1c125116.html
// http://www.ffmpeg.org/doxygen/trunk/api-example_8c-source.html
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libavcodec/avcodec.h>
#define INBUF_SIZE 4096
bool stopThread=false;  
 
int main(int argc, char **argv) {
    const char *filename; //, *outfilename;
    const AVCodec *codec;
    AVCodecParserContext *parser;
    AVCodecContext *c= NULL;
    FILE *f;
    AVFrame *frame;
    AVPacket *pkt;
    uint8_t inbuf[INBUF_SIZE + AV_INPUT_BUFFER_PADDING_SIZE];
    uint8_t *data;
    size_t   data_size;
    int ret, eof;
    filename    = argv[1];
  
    pkt = av_packet_alloc();
    if (!pkt)
        exit(1);
  
    /* set end of buffer to 0 (this ensures that no overreading happens for damaged MPEG streams) */
    memset(inbuf + INBUF_SIZE, 0, AV_INPUT_BUFFER_PADDING_SIZE);
  
    /* find the MPEG-1 video decoder */
    codec = avcodec_find_decoder(AV_CODEC_ID_MPEG1VIDEO);
    if (!codec) {
        fprintf(stderr, "Codec not found\n");
        exit(1);
    }
  
    parser = av_parser_init(codec->id);
    if (!parser) {
        fprintf(stderr, "parser not found\n");
        exit(1);
    }
   
    /* For some codecs, such as msmpeg4 and mpeg4, width and height
    MUST be initialized there because this information is not
    available in the bitstream. */
  
    /* open it */
    if (avcodec_open2(c, codec, NULL) < 0) {
        fprintf(stderr, "Could not open codec\n");
        exit(1);
    }
  
    f = fopen(filename, "rb");
    if (!f) {
        fprintf(stderr, "Could not open %s\n", filename);
        exit(1);
    }
     
    c = avcodec_alloc_context3(codec);
    if (!c) {
        fprintf(stderr, "Could not allocate video codec context\n");
        exit(1);
    }
  
    frame = av_frame_alloc();
    if (!frame) {
        fprintf(stderr, "Could not allocate video frame\n");
        exit(1);
    }
  
    do {
        /* read raw data from the input file */
        data_size = fread(inbuf, 1, INBUF_SIZE, f);
        if (ferror(f))
            break;
        eof = !data_size;
  
        /* use the parser to split the data into frames */
        data = inbuf;
        while (data_size > 0 || eof) {
            ret = av_parser_parse2(parser, c, &pkt->data, &pkt->size,
                                data, data_size, AV_NOPTS_VALUE, AV_NOPTS_VALUE, 0);
            if (ret < 0) {
                fprintf(stderr, "Error while parsing\n");
                exit(1);
            }
            data += ret;
            data_size -= ret;

            if (pkt->size) {
     			int ret;
				ret = avcodec_send_packet(c, pkt);
     			if (ret < 0) {
         			fprintf(stderr, "Error sending a packet for decoding\n");
         			exit(1);
     			}
     			while (ret >= 0) {
             		ret = avcodec_receive_frame(c, frame);
             		if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
                 		return;
             		else if (ret < 0) { 
                 		fprintf(stderr, "Error during decoding\n");
                 		exit(1);
             		}
				}

                /* put sample parameters */
                c->bit_rate = 400000;
                /* resolution must be a multiple of two */
                c->width = 352;
                c->height = 288;
                /* frames per second */
                c->time_base= (AVRational){1,25};
                c->gop_size = 10; /* emit one intra frame every ten frames */
                c->max_b_frames=1;
                c->pix_fmt = PIX_FMT_YUV420P;    

				ret = avcodec_send_frame(c, frame);
 				if (ret < 0) {
         			fprintf(stderr, "Error sending a packet for decoding\n");
         			exit(1);
 				}
										
 				while (ret >= 0) {
         			ret = avcodec_receive_packet(c, pkt);
         			if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
             			return;
         			else if (ret < 0) { 
             			fprintf(stderr, "Error during decoding\n");
             			exit(1);
         			}
				}
            else if (eof)
                 break;
         	}
        } while (!eof || stopThread);
  
    fclose(f);
  
    av_parser_close(parser);
    avcodec_free_context(&c);
    av_frame_free(&frame);
    av_packet_free(&pkt);
  
    return 0;
}

