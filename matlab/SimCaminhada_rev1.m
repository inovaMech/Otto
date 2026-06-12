robot = importrobot('Z:\home\inovamech\otto\ros2_ws\src\otto_description\urdf\otto.urdf');
config = homeConfiguration(robot);

figure;
show(robot, config, 'Frames', 'off', 'PreservePlot', false);
xlim([-0.15 0.15]); ylim([-0.15 0.15]); zlim([-0.05 0.20]);
view(45, 20);

posturas = [
    0.0   0.0   0.0   0.0;
    0.0   0.2   0.0   0.0;
    -0.3   0.2   0.0   0.0;
    -0.3   0.0   0.0   0.0;
    0.0   0.0   0.0   0.0;
    0.0   0.0   0.0   0.2;
    0.0   0.0  -0.3   0.2;
    0.0   0.0  -0.3   0.0;
    0.0   0.0   0.0   0.0;
    ];

titulos = {
    'Neutro'
    'Pe esquerdo levanta'
    'Perna esquerda recua'
    'Pe esquerdo abaixa'
    'Perna esquerda volta neutro'
    'Pe direito levanta'
    'Perna direita recua'
    'Pe direito abaixa'
    'Perna direita volta neutro'
    };

n_cycles = 3;
for c = 1:n_cycles
    for i = 1:size(posturas, 1)
        if i == 1, p_prev = posturas(end,:);
        else, p_prev = posturas(i-1,:); end
        p_next = posturas(i,:);
        steps = 8;
        for s = 1:steps
            t = s/steps;
            p = p_prev + t*(p_next - p_prev);
            config(1).JointPosition = p(1);
            config(2).JointPosition = p(2);
            config(3).JointPosition = p(3);
            config(4).JointPosition = p(4);
            show(robot, config, 'Frames', 'off', 'PreservePlot', false);
            xlim([-0.15 0.15]); ylim([-0.15 0.15]); zlim([-0.05 0.20]);
            view(45, 20);
            title(sprintf('Ciclo %d/%d - %s', c, n_cycles, titulos{i}));
            drawnow;
        end
        pause(0.1);
    end
end