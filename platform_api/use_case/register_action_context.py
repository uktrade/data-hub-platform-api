class RegisterActionContext:
    def __init__(self, action_context_gateway):
        self.action_context_gateway = action_context_gateway

    def __call__(self, id_):
        self.action_context_gateway.register_context(id_)
