%% 繪製Fx曲面
clc; clear;close all
addpath('MF62_tir_model');
%tir = load_tir("D2704_mf612.tir");
tir = load_tir("FSAE_43075R20.tir");

SL_range = linspace(-0.3,0.3,61);   % slip ratio（很重要！）
FZ_range = linspace(0,2000,61);

SA  = 0;     % 固定
IA  = 0;
P   = 80000;

cmd = "FX";

[SL_grid, FZ_grid] = meshgrid(SL_range, FZ_range);

Fx = zeros(size(SL_grid));

for i = 1:length(FZ_range)
    for j = 1:length(SL_range)

        SL = SL_grid(i,j);
        FZ = FZ_grid(i,j);

        Fx(i,j) = MF_api(cmd, FZ, SA, SL, IA, P, tir);

    end
end

figure
surf(SL_grid, FZ_grid, Fx)

xlabel('Slip Ratio')
ylabel('Normal Load Fz (N)')
zlabel('Longitudinal Force Fx (N)')
title('Magic Formula Tire Fx Surface')

colorbar
shading interp
view(45,30)

%% 峰值力量解出
[Fx_max, idx] = max(Fx, [], 2);
SL_peak = SL_range(idx);

figure
plot(FZ_range, Fx_max,'LineWidth',2)
xlabel('FZ (N)')
ylabel('Peak Fx (N)')
title('Peak Fx vs FZ')
grid on

figure
plot(FZ_range, SL_peak,'LineWidth',2)
xlabel('FZ (N)')
ylabel('Peak Slip Ratio')
title('Peak Slip Ratio vs FZ')
grid on

%% 解出摩擦係數
FZ_fit = FZ_range(:);
Fx_fit = Fx_max(:);

p1x = polyfit(FZ_fit, Fx_fit, 1);

Fx_linear = polyval(p1x, FZ_fit);

figure
plot(FZ_fit, Fx_fit,'o')
hold on
plot(FZ_fit, Fx_linear,'LineWidth',2)

xlabel('FZ (N)')
ylabel('Peak Fx (N)')
title('Linear Fit: Fx_{max} vs FZ')

legend('Data','Linear Fit')
grid on

mu_x = p1x(1);
fprintf('mu_x: %.2f\n', mu_x);