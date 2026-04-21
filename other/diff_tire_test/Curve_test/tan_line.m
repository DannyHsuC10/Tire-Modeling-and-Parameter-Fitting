clc;clear;

N = 1000;

x = -3:0.01:3;

y0 = tan(x);
y1 = sec(x).^2;
y2 = 2 * sec(x).^2 .* tan(x) ;

bx = [-pi,pi];
by = 3*bx;
figure(1)
plot(x,y0,'b','LineWidth',1)
ylabel('tan(x)')
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