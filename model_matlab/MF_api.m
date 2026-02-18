function out = MF_api(cmd, FZ, SA, SL, IA, P, mf_file) % API接口
    
    persistent MF_PARAM MF_FILE_NAME
    
    if isempty(MF_PARAM) || ~strcmp(MF_FILE_NAME, mf_file)
      
        MF_PARAM   = mf_file;

        MF_FILE_NAME = mf_file;
    end

    MF = CalculationInput(FZ, SA, SL, IA, P, MF_PARAM);
    
    switch cmd % 切換開關，套用不同模型
        case 'FX'
            out = MF612_Fx(MF);
        case 'FY'
            out = MF612_Fy(MF);
        case 'MZ'
            out = MF612_Mz(MF);
        case 'MX'
            out = MF612_Mx(MF);
        otherwise
            error("Unknown tire API command");
    end

end

function MF = CalculationInput(FZ,SA,SL,IA,P,tir_path) % 創建輸入
    tir = load_tir(tir_path);
    MF = tir;
    MF.FZ = FZ;
    MF.SA = SA;
    MF.SL = SL;
    MF.IA = IA;
    MF.pressure = P;
    % 調整變數命名
    MF.PIO = tir.NOMPRES;
    MF.FZO = tir.FNOMIN;
    MF.Ro = tir.UNLOADED_RADIUS;
    % 預設速度
    MF.V = tir.LONGVL;  
    % 固定參數
    MF.lambdaFzo=1;        %λFzo   (nominal (rated) load) 
    MF.lambdaMuyMi=1;      %λμy*   (peak friction coefficient) 這之後實際使用要改0.6
    MF.lambdyMuyPrime=1;   %λμy'   (peak friction coefficient)
    MF.lambdaKya=1;        %λKya   (cornering stiffness)
    MF.lambdaCy=1;         %λCy    (shape factor)
    MF.lambdaEy=1;         %λEy    (curvature factor)
    MF.lambdaHy=1;         %λHy    (horizontal shift)
    MF.lambdaVy=1;         %λVy    (vertical shift)
    MF.lambdaKyia=1;       %λKyγ   (camber force stiffness)
    MF.lambdat=1;          %λt   
    MF.lambdaKzia=1;
    MF.lambdaMr=1;
    MF.lambdaS=1;
    MF.lambdaYk=1;
    MF.lambdaVyk=1;
    MF.lambdaHx=1;
    MF.lambdaVx=1;
    MF.lambdaMuxPrime=1;
    MF.lambdaKxk=1;
    MF.lambdaEx=1;
    MF.lambdaMuxMi=1; % 這之後實際使用要改0.6
    MF.lambdaCx=1;
    MF.lambdaXa=1;
    MF.lambdaVMX = 1;
    MF.lambdaMX = 1;
    MF.zeta1=1;
    % 調整參數
    MF.zeta0=1;
    MF.zeta2=1;
    MF.zeta3=1;
    MF.zeta4=1;
    MF.zeta5=1;
    MF.zeta6=1;
    MF.zeta7=1;
    MF.zeta8=1;
    MF.epsilonK=0.1;
    % 穩定參數
    MF.epsilonY=0.1;
    MF.epsilonX=0.1;
end

function val = parse_value(valueStr) % 解析數值
    % 嘗試把字串轉成數值，失敗則保留字串
    num = str2double(valueStr);
    if ~isnan(num)
        val = num;
    else
        val = valueStr;
    end
end

function tir_params = load_tir(filepath) % 載入tir
     
    % 初始化 struct
    tir_params = struct();
    
    % 開啟檔案
    fid = fopen(filepath, 'r', 'n', 'UTF-8');
    if fid == -1
        error('無法開啟檔案: %s', filepath);
    end
    
    % 逐行讀取
    while ~feof(fid)
        line = strtrim(fgetl(fid));
        
        % 忽略空行
        if isempty(line)
            continue;
        end
        
        % 忽略註解
        if startsWith(line, '$')
            continue;
        end
        
        % 忽略 section header
        if startsWith(line, '[') && endsWith(line, ']')
            continue;
        end
        
        % 移除行內註解
        dollarPos = strfind(line, '$');
        if ~isempty(dollarPos)
            line = strtrim(line(1:dollarPos(1)-1));
        end
        
        % 必須包含 '='
        eqPos = strfind(line, '=');
        if isempty(eqPos)
            continue;
        end
        
        % 分割 key 與 value
        key = strtrim(line(1:eqPos(1)-1));
        valueStr = strtrim(line(eqPos(1)+1:end));
        
        % 嘗試轉換數值
        value = parse_value(valueStr);
        
        % 存入 struct
        % 注意：MATLAB struct 的欄位名稱必須是合法識別字
        % 如果 key 有非法字元，可以用 matlab.lang.makeValidName
        key = matlab.lang.makeValidName(key);
        tir_params.(key) = value;
    end
    
    fclose(fid);
end

