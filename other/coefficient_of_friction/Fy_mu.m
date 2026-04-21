% 啟動設定
clc; clear;close all
addpath('MF62_tir_model');
tir = load_tir("D2704_mf612.tir");
%tir = load_tir("FSAE_43075R20.tir");

%% 繪製Fy曲面
% 掃描範圍
SA_range = linspace(-15,15,61);      % Slip Angle (deg)
FZ_range = linspace(0,2000,61);      % Normal Load (N)

% 固定參數
SL  = 0;        % slip ratio
IA  = 0;        % camber angle
P   = 80000;        % pressure

cmd = "FY";     % MF輸出：側向力

% 建立網格
[SA_grid, FZ_grid] = meshgrid(SA_range, FZ_range);

Fy = zeros(size(SA_grid));

% 掃描計算
for i = 1:length(FZ_range)
    for j = 1:length(SA_range)

        SA = SA_grid(i,j);
        FZ = FZ_grid(i,j);

        Fy(i,j) = MF_api(cmd, FZ, SA, SL, IA, P, tir);

    end
end

% 畫曲面
figure
surf(SA_grid, FZ_grid, Fy)

xlabel('Slip Angle (deg)')
ylabel('Normal Load Fz (N)')
zlabel('Lateral Force Fy (N)')

title('Magic Formula Tire Fy Surface')
colorbar
shading interp
view(45,30)

%% 畫圖

[Fy_max, idx] = max(Fy, [], 2);   % 每個FZ找最大Fy
SA_peak = SA_range(idx);          % 對應的滑移角

figure
plot(FZ_range, Fy_max,'LineWidth',2)

xlabel('Normal Load Fz (N)')
ylabel('Peak Lateral Force Fy (N)')
title('Peak Fy vs Normal Load')
grid on

figure
plot(FZ_range, SA_peak,'LineWidth',2)

xlabel('Normal Load Fz (N)')
ylabel('Peak Slip Angle (deg)')
title('Peak Slip Angle vs Normal Load')
grid on

%% 線性回歸（正確版本）

% =========================
% 1️ Peak Fy vs FZ（這段是正確的）
% =========================
FZ_fit = FZ_range(:);
Fy_fit = Fy_max(:);

p1 = polyfit(FZ_fit, Fy_fit, 1);
Fy_linear = polyval(p1, FZ_fit);

figure
plot(FZ_fit, Fy_fit,'o')
hold on
plot(FZ_fit, Fy_linear,'LineWidth',2)

xlabel('FZ (N)')
ylabel('Peak Fy (N)')
title('Linear Fit: Fy_{max} vs FZ')

legend('Data','Linear Fit')
grid on

%% 印出
mu = p1(1);
fprintf('mu: %.2f\n',mu)
