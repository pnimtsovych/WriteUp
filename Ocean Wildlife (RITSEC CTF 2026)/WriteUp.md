<img width="1187" height="90" alt="image" src="https://github.com/user-attachments/assets/379d20e5-f117-43c4-8567-c205ac8431e6" />

After unpacking the archive, the metadata.yaml and mystery_message_0.db3 files became visible, which pointed to a ROS2 bag in SQLite format.

<img width="1919" height="979" alt="image" src="https://github.com/user-attachments/assets/42a2a999-3e71-4d4d-927a-0d614002f560" />

After opening metadata.yaml, a list of topics inside the ROS2 bag became visible. Among the standard topics, such as /turtle1/pose and /turtle1/color_sensor, the /draw_commands topic of type std_msgs/msg/String stood out, containing 284 messages. It was this topic that looked the most suspicious, since its name directly hinted at drawing commands. This suggested that the hidden message was not stored as plain text, but was formed through a sequence of commands for turtlesim, which had to be extracted from .db3 and reproduced.


After identifying /draw_commands as the most relevant topic, I wrote a Python script solve.py to extract its messages from mystery_message_0.db3. Since the bag file uses SQLite, I accessed it through Python’s built-in sqlite3 module, queried the topics table to get the ID of /draw_commands, and then selected all corresponding records from the messages table in timestamp order. The stored message data was serialized as ROS2 std_msgs/msg/String, so I decoded each blob to recover the original JSON commands. These commands contained actions such as teleport and pen, which described how the turtlesim turtle moved and whether it was drawing. I then reproduced this movement by rendering lines between coordinates whenever the pen was enabled. After processing the full sequence, the generated image revealed the hidden flag.

<img width="903" height="903" alt="image" src="https://github.com/user-attachments/assets/00c66274-6b74-4c48-866f-8ff07261c611" />

## FLAG: RS{f0LL0w_th3_5ea_Turtles}

