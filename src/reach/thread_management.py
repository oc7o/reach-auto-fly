import queue

message_queues = {
    "mqtt_listener_daemon": queue.Queue(),
    "flight_controller_daemon": queue.Queue(),
    "recognition_model_daemon": queue.Queue(),
}
