class BUTTON:
    """
    Button Error messages.
    """

    def __init__(self):
        self.messages = [
            "Error: Something went wrong!",
            "Warning: Please check your input.",
            "Info: Action completed successfully.",
            "Notice: This is a notice message.",
            "Alert: Please pay attention to this."
        ]
        self.current_index = 0

    def get_next_message(self):
        message = self.messages[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.messages)
        return message