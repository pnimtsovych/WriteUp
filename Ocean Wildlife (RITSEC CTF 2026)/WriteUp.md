<img width="1187" height="90" alt="image" src="https://github.com/user-attachments/assets/379d20e5-f117-43c4-8567-c205ac8431e6" />

After unpacking the archive, the metadata.yaml and mystery_message_0.db3 files became visible, which pointed to a ROS2 bag in SQLite format.

<img width="1919" height="979" alt="image" src="https://github.com/user-attachments/assets/42a2a999-3e71-4d4d-927a-0d614002f560" />

After opening metadata.yaml, a list of topics inside the ROS2 bag became visible. Among the standard topics, such as /turtle1/pose and /turtle1/color_sensor, the /draw_commands topic of type std_msgs/msg/String stood out, containing 284 messages. It was this topic that looked the most suspicious, since its name directly hinted at drawing commands. This suggested that the hidden message was not stored as plain text, but was formed through a sequence of commands for turtlesim, which had to be extracted from .db3 and reproduced.

