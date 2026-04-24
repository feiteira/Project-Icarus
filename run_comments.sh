#!/bin/bash
python3 -u post_discussion_comments.py 1 > /tmp/post_comments_output.txt 2>&1
echo "DONE_EXIT:$?" >> /tmp/post_comments_output.txt