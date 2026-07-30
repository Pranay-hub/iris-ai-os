from app.capabilities.system.capability import SystemCapability


class CapabilityRegistry:
    def __init__(self):
        self.capabilities = {}
        self.register(SystemCapability())

    def register(self, capability):
        self.capabilities[capability.name] = capability

    def list_capabilities(self):
        return [
            capability.manifest()
            for capability in self.capabilities.values()
        ]

    def get(self, name: str):
        capability = self.capabilities.get(name)

        if capability is None:
            raise ValueError(f"Capability not found: {name}")

        return capability