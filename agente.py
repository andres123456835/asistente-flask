import torch
import torch.nn as nn
import torch.optim as optim

class RedNeuronal(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(RedNeuronal, self).__init__()
        self.modelo = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, output_dim)
        )

    def forward(self, x):
        return self.modelo(x)

class Agente:
    def __init__(self, estado_dim, accion_dim):
        self.modelo = RedNeuronal(estado_dim, accion_dim)
        self.optim = optim.Adam(self.modelo.parameters(), lr=0.01)
        self.loss_fn = nn.MSELoss()

    def elegir_accion(self, estado):
        with torch.no_grad():
            estado_tensor = torch.tensor(estado)
            q_vals = self.modelo(estado_tensor)
            return torch.argmax(q_vals).item()

    def entrenar(self, estado, accion, recompensa, estado_siguiente):
        estado_tensor = torch.tensor(estado)
        siguiente_tensor = torch.tensor(estado_siguiente)

        q_vals = self.modelo(estado_tensor)
        q_siguiente = self.modelo(siguiente_tensor).detach()

        objetivo = q_vals.clone()
        objetivo[accion] = recompensa + 0.9 * torch.max(q_siguiente)

        loss = self.loss_fn(q_vals, objetivo)

        self.optim.zero_grad()
        loss.backward()
        self.optim.step()
