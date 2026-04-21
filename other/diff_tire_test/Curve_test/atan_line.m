clc;clear;

N = 1000;

x = -1.5:0.01:1.5;

y0 = atan(x);
y1 = 1./(1+x.^2);
y2 = -2*x./(1+x.^2).^2;

bx = [-4,4];
by = 3*bx;

figure(1)
plot(x,y0,'b','LineWidth',1)
ylabel('tan(x)')
title('tan(x)')
xlim(bx)
ylim(by)
grid on
figure(2)
plot(x,y1,'r','LineWidth',1)
ylabel('d/dx tan(x) = sec^2(x)')
xlim(bx)
ylim(by)
grid on
figure(3)
plot(x,y2,'g','LineWidth',1)
ylabel('d^2/dx^2 tan(x)')
xlabel('x')
xlim(bx)
ylim(by)
grid on