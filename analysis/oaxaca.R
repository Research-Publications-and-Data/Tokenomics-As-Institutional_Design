library(oaxaca)

setwd("/Users/zach/b2-governance-data")

# ── Load data ─────────────────────────────────────────────────────────────────
reg <- read.csv("data/regression_data_april2026.csv", stringsAsFactors = FALSE)

# Filter to regression-ready DeFi and DePIN only
df <- reg[reg$regression_ready == "True" & reg$category %in% c("DeFi", "DePIN"), ]
cat("DeFi N =", sum(df$category == "DeFi"), "\n")
cat("DePIN N =", sum(df$category == "DePIN"), "\n")
cat("Total N =", nrow(df), "\n\n")

# Variables
df$is_depin      <- as.integer(df$category == "DePIN")
df$age_years     <- as.numeric(df$maturity_years)
df$log_fdv       <- as.numeric(df$log_fdv)
df$insider_pct   <- as.numeric(df$insider_pct)
df$subsidy_ratio <- as.numeric(df$subsidy_ratio)

# Impute subsidy_ratio median for Oaxaca (requires complete cases)
med_sub <- median(df$subsidy_ratio, na.rm = TRUE)
df$subsidy_ratio_imp <- ifelse(is.na(df$subsidy_ratio), med_sub, df$subsidy_ratio)

cat("Complete cases for decomposition vars:\n")
print(colSums(is.na(df[, c("hhi","age_years","log_fdv","insider_pct","subsidy_ratio_imp","is_depin")])))
cat("\n")

# ── Oaxaca-Blinder ─────────────────────────────────────────────────────────────
set.seed(42)
ob <- oaxaca(
  hhi ~ age_years + log_fdv + insider_pct + subsidy_ratio_imp | is_depin,
  data = df,
  R    = 500
)

cat("=== OAXACA-BLINDER SUMMARY ===\n")
print(ob)

cat("\n=== TWOFOLD OVERALL ===\n")
overall <- ob$twofold$overall
print(round(overall, 6))

gap         <- ob$y$y.A - ob$y$y.B
explained   <- overall[1, "coef(explained)"]
unexplained <- overall[1, "coef(unexplained)"]

cat(sprintf("\nDePIN mean HHI:  %.4f\n", ob$y$y.A))
cat(sprintf("DeFi mean HHI:   %.4f\n",  ob$y$y.B))
cat(sprintf("Raw gap:         %.4f\n",  gap))
cat(sprintf("Explained:       %.4f  (%.1f%% of gap)\n", explained,   explained/gap*100))
cat(sprintf("Unexplained:     %.4f  (%.1f%% of gap)\n", unexplained, unexplained/gap*100))

# Save overall
results <- data.frame(
  component  = c("DePIN mean", "DeFi mean", "Overall gap", "Explained", "Unexplained"),
  estimate   = c(ob$y$y.A, ob$y$y.B, gap, explained, unexplained),
  pct_of_gap = c(NA, NA, 100, round(explained/gap*100,1), round(unexplained/gap*100,1))
)
write.csv(results, "data/oaxaca_decomposition_results.csv", row.names = FALSE)

# Detailed per-variable contributions
cat("\n=== VARIABLE CONTRIBUTIONS ===\n")
detail <- ob$twofold$variables
if (!is.null(detail)) {
  d <- as.data.frame(detail[[1]])
  print(round(d, 5))
  write.csv(d, "data/oaxaca_detailed_decomposition.csv", row.names = FALSE)
}

cat("\nSaved oaxaca_decomposition_results.csv\n")
cat("Saved oaxaca_detailed_decomposition.csv\n")
