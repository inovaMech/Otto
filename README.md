# Otto

Ambiente de simulação do robô Otto para a disciplina.

**Stack:** ROS 2 Jazzy · Gazebo Harmonic · Octave · Docker

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- Windows 11 com WSL2 (recomendado) **ou** Linux nativo
- Windows 10: instalar [VcXsrv](https://sourceforge.net/projects/vcxsrv/) para display gráfico

---

## Como usar

```bash
# 1. Clonar o repositório
git clone https://github.com/inovamech/otto.git
cd otto

# 2. Subir o container
cd docker
docker compose up -d

# 3. Entrar no container
docker exec -it otto bash

# 4. Visualizar o URDF (sem ROS, hot reload)
urdf-viz /ros2_ws/src/otto_description/urdf/otto.urdf

# 5. Visualizar no RViz2
ros2 launch otto_description display.launch.py

# 6. Simulação completa no Gazebo
ros2 launch otto_description gazebo.launch.py
```

---

## Estrutura do repositório

```
otto/
├── docker/          → Dockerfile, docker-compose.yml, entrypoint
├── ros2_ws/src/
│   └── otto_description/
│       ├── urdf/    → otto.urdf
│       ├── meshes/  → arquivos .stl
│       └── launch/  → display.launch.py, gazebo.launch.py
├── octave/
│   └── exercicios/  → scripts .m dos alunos
└── docs/
```

---

## Validação rápida do URDF

```bash
# Verificar sintaxe e árvore de joints
check_urdf /ros2_ws/src/otto_description/urdf/otto.urdf

# Gerar gráfico da árvore cinemática
urdf_to_graphviz /ros2_ws/src/otto_description/urdf/otto.urdf
```