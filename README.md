# Otto

Ambiente de modelagem, visualização e simulação do robô Otto utilizado na disciplina. O projeto integra Fusion 360, ROS 2 e Gazebo para validar a estrutura mecânica, a cinemática e os algoritmos de controle antes da implementação em hardware.

**Stack:** ROS 2 Jazzy · Gazebo Harmonic · Octave · Docker

---

## Fluxo de desenvolvimento

```text
Fusion 360 (.f3d/.f3z)
        ↓
Exportação STL
        ↓
URDF/Xacro
        ↓
RViz2
        ↓
Gazebo
        ↓
Controle ROS 2
```

O robô é modelado no Fusion 360, exportado como malhas STL e descrito em URDF/Xacro. A validação inicial é realizada no RViz e, posteriormente, a simulação física é executada no Gazebo.

---

## Pré-requisitos

* Docker Desktop
* Windows 11 com WSL2 (recomendado) ou Linux
* Windows 10: VcXsrv para suporte gráfico

---

## Como usar

```bash
# Clonar o repositório
git clone https://github.com/inovamech/otto.git
cd otto

# Iniciar o ambiente
cd docker
docker compose up -d

# Entrar no container
docker exec -it otto bash

# Visualizar o modelo
urdf-viz /ros2_ws/src/otto_description/urdf/otto.urdf

# Abrir no RViz
ros2 launch otto_description display.launch.py

# Executar no Gazebo
ros2 launch otto_description gazebo.launch.py
```

---

## Estrutura do repositório

```text
otto/
├── docker/
├── ros2_ws/
│   └── src/
│       └── otto_description/
│           ├── urdf/
│           ├── meshes/
│           ├── config/
│           └── launch/
├── octave/
└── docs/
```

---

## Principais arquivos

### Fusion 360

* **.f3d**: arquivo nativo do Fusion 360.
* **.f3z**: pacote contendo montagens e dependências.
* **.stl**: malhas 3D exportadas para o ROS e Gazebo.

### Descrição do robô

* **.urdf**: estrutura cinemática do robô (links e juntas).
* **.xacro**: versão parametrizada do URDF com reutilização de código.

### Configuração

* **.yaml**: parâmetros de controladores, Gazebo e ROS 2.

### Inicialização

* **display.launch.py**: carrega o modelo no RViz.
* **gazebo.launch.py**: inicia a simulação no Gazebo.
* **control.launch.py**: inicia controladores e nós auxiliares.

### Visualização e simulação

* **.rviz**: configuração do ambiente RViz.
* **.world**: cenário de simulação do Gazebo.
* **.sdf**: formato nativo utilizado internamente pelo Gazebo.

### Controle

* **.py**: nós ROS 2 para controle, sensores e algoritmos.
* **.m**: scripts Octave/MATLAB para estudos de cinemática e controle.

### Infraestrutura

* **Dockerfile**: define a imagem do ambiente.
* **docker-compose.yml**: automatiza a execução dos containers.
* **entrypoint.sh**: configura o ambiente ao iniciar o container.

---

## Validação do modelo

Verificar a estrutura do URDF:

```bash
check_urdf /ros2_ws/src/otto_description/urdf/otto.urdf
```

Gerar a árvore cinemática:

```bash
urdf_to_graphviz /ros2_ws/src/otto_description/urdf/otto.urdf
```

Essas verificações ajudam a identificar problemas de modelagem antes da execução no RViz ou Gazebo.
