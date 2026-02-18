%這部分是連接matlab的橋梁，透過輸出mat檔案到其他matlab模型進行重複測試
clc;clear;close all;
%% 1. 載入原始 mat 檔

orig_file = 'MF612_parameter_new.mat';
load(orig_file);

%% 2. 載入 CSV

% 取得目前程式所在資料夾
currentFolder = fileparts(mfilename('fullpath'));

% 指定資料夾
dataFolder = fullfile(fileparts(currentFolder), 'data', 'Fitting_data');

% 指定檔案
filename = fullfile(dataFolder, 'Fitting_process.csv');

% 讀取 CSV
T = readtable(filename);

% Initialize parameters structure
params = struct();
for i = 1:height(T)
    params.(T.name{i}) = T.x0(i);
    fprintf("%s >> %g\n",T.name{i},T.x0(i))
end
%% 3.設定資料型態
Px = [params.PCX1,params.PDX1,params.PDX2,params.PDX3,params.PEX1,params.PEX2,params.PEX3,params.PEX4,params.PKX1,params.PKX2,...
        params.PKX3,params.PHX1,params.PHX2,params.PVX1,params.PVX2,params.PPX1,params.PPX2,params.PPX3,params.PPX4];

Rx = [params.RBX1,params.RBX2,params.RBX3,params.RCX1,params.REX1,params.REX2,params.RHX1];

Py = [params.PCY1,params.PDY1,params.PDY2,params.PDY3,params.PEY1,params.PEY2,params.PEY3,params.PEY4,params.PEY5,params.PKY1,...
        params.PKY2,params.PKY3,params.PKY4,params.PKY5,params.PKY6,params.PKY7,params.PHY1,params.PHY2,params.PVY1,params.PVY2,...
        params.PVY3,params.PVY4,params.PPY1,params.PPY2,params.PPY3,params.PPY4,params.PPY5];

Ry = [params.RBY1,params.RBY2,params.RBY3,params.RBY4,params.RCY1,params.REY1,params.REY2,params.RHY1,params.RHY2,params.RVY1,...
    params.RVY2,params.RVY3,params.RVY4,params.RVY5,params.RVY6];

%% 4. 儲存成新的 mat 檔
new_file = 'MF612_parameter_new.mat';
save(new_file);  % 會自動把 Workspace 裡所有變數（包含更新後的 Px,Py,Rx,Ry）存進去

disp(['修改完成，已存成: ', new_file]);