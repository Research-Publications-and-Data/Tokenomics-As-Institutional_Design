library(fixest)
library(modelsummary)
library(ggplot2)
library(dplyr)
library(tidyr)

setwd("/Users/zach/b2-governance-data")

# ── Load data ─────────────────────────────────────────────────────────────────
full <- read.csv("data/full_merged_dataset.csv", stringsAsFactors = FALSE)
full <- full[full$regression_ready == "True", ]

full$age_years     <- as.numeric(full$maturity_years)
full$log_fdv       <- as.numeric(full$log_fdv)
full$log_revenue   <- as.numeric(full$log_revenue)
full$insider_pct   <- as.numeric(full$insider_pct)
full$subsidy_ratio <- as.numeric(full$subsidy_ratio)
full$hhi           <- as.numeric(full$hhi)
full$category      <- factor(full$category, levels = c("DeFi","DePIN","L1_L2_Infra","Social_Dead"))
full$governance_model <- as.factor(full$governance_model)

cat("Full sample N =", nrow(full), "\n")
cat("Category breakdown:\n"); print(table(full$category))

# ── Regression models ──────────────────────────────────────────────────────────
m1 <- lm(hhi ~ category,                                                       data = full)
m2 <- lm(hhi ~ category + age_years + log_fdv,                                 data = full)
m3 <- lm(hhi ~ category + age_years + log_fdv + insider_pct,                   data = full)
m4 <- lm(hhi ~ category + age_years + log_fdv + insider_pct + subsidy_ratio,   data = full)
m5 <- lm(hhi ~ category + age_years + log_fdv + insider_pct + subsidy_ratio + governance_model + log_revenue,
         data = full)

# Print summaries
for (i in 1:5) {
  cat(sprintf("\n=== Model %d ===\n", i))
  print(summary(get(sprintf("m%d", i))))
}

# Publication table
modelsummary(
  list("(1)" = m1, "(2)" = m2, "(3)" = m3, "(4)" = m4, "(5)" = m5),
  stars      = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
  gof_omit   = "AIC|BIC|Log|F$",
  coef_rename = c(
    "categoryDePIN"            = "DePIN (vs DeFi)",
    "categoryL1_L2_Infra"      = "L1/L2/Infra (vs DeFi)",
    "categorySocial_Dead"      = "Social/Dead (vs DeFi)",
    "age_years"                = "Protocol Age (years)",
    "log_fdv"                  = "Log FDV",
    "insider_pct"              = "Initial Insider %",
    "subsidy_ratio"            = "Subsidy Ratio",
    "governance_modelfutarchy" = "Futarchy",
    "governance_modeltoken_weighted" = "Token-Weighted",
    "log_revenue"              = "Log Revenue"
  ),
  output = "data/full_regression_table.html"
)
cat("Saved full_regression_table.html\n")

# Also save as markdown for quick reading
modelsummary(
  list("(1)" = m1, "(2)" = m2, "(3)" = m3, "(4)" = m4, "(5)" = m5),
  stars      = c("*" = 0.10, "**" = 0.05, "***" = 0.01),
  gof_omit   = "AIC|BIC|Log|F$",
  coef_rename = c(
    "categoryDePIN"            = "DePIN (vs DeFi)",
    "categoryL1_L2_Infra"      = "L1/L2/Infra (vs DeFi)",
    "categorySocial_Dead"      = "Social/Dead (vs DeFi)",
    "age_years"                = "Protocol Age (years)",
    "log_fdv"                  = "Log FDV",
    "insider_pct"              = "Initial Insider %",
    "subsidy_ratio"            = "Subsidy Ratio",
    "governance_modelfutarchy" = "Futarchy",
    "governance_modeltoken_weighted" = "Token-Weighted",
    "log_revenue"              = "Log Revenue"
  ),
  output = "data/full_regression_table.txt"
)

# ── Exhibit: Initial allocation → HHI scatter ─────────────────────────────────
p1 <- ggplot(full[!is.na(full$insider_pct), ],
             aes(x = insider_pct, y = hhi, color = category, label = protocol)) +
  geom_smooth(aes(group = 1), method = "lm", se = TRUE,
              color = "gray40", linetype = "dashed", linewidth = 0.8) +
  geom_point(size = 3) +
  ggrepel::geom_text_repel(size = 2.5, max.overlaps = 20, segment.color = "gray70") +
  scale_color_manual(values = c("DeFi" = "#1f4e79", "DePIN" = "#c00000",
                                "L1_L2_Infra" = "#375623", "Social_Dead" = "#7f7f7f")) +
  labs(x = "Initial Insider Allocation (%)", y = "Governance Token HHI (April 2026)",
       title  = "Initial Token Allocation Predicts Current Governance Concentration",
       color  = "Category") +
  theme_minimal(base_family = "serif") +
  theme(text = element_text(size = 11))

# Install ggrepel if needed
if (!requireNamespace("ggrepel", quietly = TRUE)) {
  install.packages("ggrepel", repos = "https://cloud.r-project.org")
}
library(ggrepel)

p1 <- ggplot(full[!is.na(full$insider_pct), ],
             aes(x = insider_pct, y = hhi, color = category, label = protocol)) +
  geom_smooth(aes(group = 1), method = "lm", se = TRUE,
              color = "gray40", linetype = "dashed", linewidth = 0.8) +
  geom_point(size = 3) +
  geom_text_repel(size = 2.5, max.overlaps = 20, segment.color = "gray70") +
  scale_color_manual(values = c("DeFi" = "#1f4e79", "DePIN" = "#c00000",
                                "L1_L2_Infra" = "#375623", "Social_Dead" = "#7f7f7f")) +
  labs(x = "Initial Insider Allocation (%)", y = "Governance Token HHI (April 2026)",
       title  = "Initial Token Allocation Predicts Current Governance Concentration",
       color  = "Category") +
  theme_minimal(base_family = "serif") +
  theme(text = element_text(size = 11))
ggsave("data/exhibit_initial_allocation.png", p1, width = 10, height = 6, dpi = 300)
cat("Saved exhibit_initial_allocation.png\n")

# ── Exhibit: Raw vs delegated HHI ─────────────────────────────────────────────
deleg <- read.csv("data/delegation_adjusted_hhi.csv")
# Also pull Snapshot voting HHI
vhhi  <- read.csv("data/voting_hhi.csv")

# Build long frame: raw token HHI vs effective voting HHI
# For Tally protocols use delegated_hhi; for Snapshot use voting_hhi
eff <- data.frame(
  protocol = character(), raw_hhi = numeric(), eff_hhi = numeric(), source = character()
)
for (i in seq_len(nrow(deleg))) {
  eff <- rbind(eff, data.frame(
    protocol = deleg$protocol[i],
    raw_hhi  = deleg$raw_hhi[i],
    eff_hhi  = deleg$delegated_hhi[i],
    source   = "Tally (delegate)",
    stringsAsFactors = FALSE
  ))
}
for (i in seq_len(nrow(vhhi))) {
  if (vhhi$source[i] == "snapshot") {
    proto <- full$protocol[full$token == vhhi$symbol[i]]
    if (length(proto) == 0) proto <- vhhi$symbol[i]
    eff <- rbind(eff, data.frame(
      protocol = proto[1],
      raw_hhi  = vhhi[i, "voting_hhi"],
      eff_hhi  = vhhi[i, "voting_hhi"],
      source   = "Snapshot (voting)",
      stringsAsFactors = FALSE
    ))
  }
}

long_deleg <- deleg %>%
  select(protocol, raw_hhi, delegated_hhi) %>%
  pivot_longer(cols = c(raw_hhi, delegated_hhi), names_to = "type", values_to = "hhi")

p2 <- ggplot(long_deleg, aes(x = reorder(protocol, -hhi), y = hhi, fill = type)) +
  geom_col(position = "dodge") +
  labs(x = "", y = "HHI",
       title = "Token-Holder vs Delegate Governance Concentration",
       fill  = "") +
  scale_fill_manual(values = c("raw_hhi" = "#c00000", "delegated_hhi" = "#1f4e79"),
                    labels  = c("Delegated HHI", "Raw Token HHI")) +
  coord_flip() +
  theme_minimal(base_family = "serif") +
  theme(text = element_text(size = 11))
ggsave("data/exhibit_delegation_adjusted.png", p2, width = 10, height = 5, dpi = 300)
cat("Saved exhibit_delegation_adjusted.png\n")

# ── Exhibit: HHI vs governance participation ──────────────────────────────────
part <- read.csv("data/governance_participation.csv")
part_merged <- merge(
  full[, c("protocol","token","category","hhi")],
  part[, c("symbol","n_voters_sampled","governance_source")],
  by.x = "token", by.y = "symbol", all.x = TRUE
)
part_merged <- part_merged[!is.na(part_merged$n_voters_sampled) & part_merged$n_voters_sampled > 0, ]

p3 <- ggplot(part_merged, aes(x = hhi, y = n_voters_sampled, color = category, label = protocol)) +
  geom_point(size = 3) +
  geom_smooth(aes(group = 1), method = "lm", se = TRUE,
              color = "gray40", linetype = "dashed", linewidth = 0.8) +
  geom_text_repel(size = 2.5, max.overlaps = 15, segment.color = "gray70") +
  scale_y_log10() +
  scale_color_manual(values = c("DeFi" = "#1f4e79", "DePIN" = "#c00000",
                                "L1_L2_Infra" = "#375623", "Social_Dead" = "#7f7f7f")) +
  labs(x = "Governance Token HHI", y = "Unique Voters per Proposal (log scale)",
       title = "Governance Concentration and Participation",
       color = "Category") +
  theme_minimal(base_family = "serif") +
  theme(text = element_text(size = 11))
ggsave("data/exhibit_concentration_participation.png", p3, width = 10, height = 6, dpi = 300)
cat("Saved exhibit_concentration_participation.png\n")

cat("\nAll W7 outputs saved.\n")
