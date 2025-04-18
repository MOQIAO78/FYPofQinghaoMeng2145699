library(readxl)
library(dplyr)
library(ggplot2)

# 读取真实世界数据与模拟数据
real <- read_excel("real_ca.xlsx")
sim <- read_excel("sim_ca.xlsx")

# 计算每个R0值下模拟数据与真实数据的误差infection/clinical/recovered/death
##Infection
mse1 <- sim %>%
  group_by(R0) %>%
  # 以Year为关键字段合并真实数据
  left_join(real, by = "Year", suffix = c("_sim", "_real")) %>%
  # 计算各年Infection状态的均方误差，na.rm用于排除缺失数据
  summarize(MSE = mean((Infection_sim - Infection_real)^2, na.rm = TRUE))
print(mse1)

# 绘制R0与MSE的关系图
ggplot(mse1, aes(x = R0, y = MSE)) +
  geom_line() +
  geom_point() +
  labs(title = "Basic reproduction number (R0) VS. Infection",
       x = "Basic reproduction number (R0)",
       y = "Mean Squared Error (MSE)") +
  theme_minimal()

##Clinical
mse2 <- sim %>%
  group_by(R0) %>%
  # 以Year为关键字段合并真实数据
  left_join(real, by = "Year", suffix = c("_sim", "_real")) %>%
  # 计算各年Clinical状态的均方误差
  summarize(MSE = mean((Clinical_sim - Clinical_real)^2, na.rm = TRUE))
print(mse2)

# 绘制R0与MSE的关系图
ggplot(mse1, aes(x = R0, y = MSE)) +
  geom_line() +
  geom_point() +
  labs(title = "Basic reproduction number (R0) VS. Clinical ",
       x = "Basic reproduction number (R0)",
       y = "Mean Squared Error (MSE)") +
  theme_minimal()

##Recovered
mse3 <- sim %>%
  group_by(R0) %>%
  # 以Year为关键字段合并真实数据
  left_join(real, by = "Year", suffix = c("_sim", "_real")) %>%
  # 计算各年Clinical状态的均方误差，na.rm用于排除缺失数据
  summarize(MSE = mean((Recovered_sim - Recovered_real)^2, na.rm = TRUE))
print(mse3)

# 绘制R0与MSE的关系图
ggplot(mse3, aes(x = R0, y = MSE)) +
  geom_line() +
  geom_point() +
  labs(title = "Basic reproduction number (R0) VS. Recovered",
       x = "Basic reproduction number (R0)",
       y = "Mean Squared Error (MSE)") +
  theme_minimal()

##Death
mse4 <- sim %>%
  group_by(R0) %>%
  # 以Year为关键字段合并真实数据
  left_join(real, by = "Year", suffix = c("_sim", "_real")) %>%
  # 计算各年Clinical状态的均方误差，na.rm用于排除缺失数据
  summarize(MSE = mean((Death_sim - Death_real)^2, na.rm = TRUE))
print(mse4)

# 绘制R0与MSE的关系图
ggplot(mse4, aes(x = R0, y = MSE)) +
  geom_line() +
  geom_point() +
  labs(title = "Basic reproduction number (R0) VS. Death",
       x = "Basic reproduction number (R0)",
       y = "Mean Squared Error (MSE)") +
  theme_minimal()

#Results
best_R0_Infection <- mse1 %>%
  filter(MSE == min(MSE, na.rm = TRUE))
best_R0_Clinical <- mse2 %>%
  filter(MSE == min(MSE, na.rm = TRUE))
best_R0_Recovered <- mse3 %>%
  filter(MSE == min(MSE, na.rm = TRUE))
best_R0_Death <- mse4 %>%
  filter(MSE == min(MSE, na.rm = TRUE))
cat("Infection Best R0：", best_R0_Infection$R0)
cat("Clinical Best R0：", best_R0_Clinical$R0)
cat("Recovered Best R0：", best_R0_Recovered$R0)
cat("Death Best R0：", best_R0_Death$R0)
