class GetContextualActions:
    def __init__(self, action_context_gateway):
        self.action_context_gateway = action_context_gateway

    def __call__(self, context_id):
        context = self.action_context_gateway.get_context(context_id)
        if context is None:
            return {
                'success': False,
                'errors': ['NO_ACTION_CONTEXT_DEFINED']

            }

        return {
            'success': True,
            'actions': []
        }