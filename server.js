const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static('public'));

/**
 * POST /api/calculate-loewe
 * Body: { DA: number, DB: number, dA: number, dB: number }
 */
app.post('/api/calculate-loewe', (req, res) => {
  const { DA, DB, dA, dB } = req.body;

  if (!DA || !DB || DA <= 0 || DB <= 0 || dA < 0 || dB < 0) {
    return res.status(400).json({ error: 'Invalid or missing dose parameters.' });
  }

  const fracA = dA / DA;
  const fracB = dB / DB;
  const ci = fracA + fracB;

  let classification = 'Additive';
  let description = 'Additive interaction (0.9 <= CI <= 1.1)';

  if (ci < 0.9) {
    classification = 'Synergistic';
    description = 'Synergistic interaction (CI < 0.9)';
  } else if (ci > 1.1) {
    classification = 'Antagonistic';
    description = 'Antagonistic interaction (CI > 1.1)';
  }

  res.json({
    DA,
    DB,
    dA,
    dB,
    fraction_A: Number(fracA.toFixed(4)),
    fraction_B: Number(fracB.toFixed(4)),
    combination_index: Number(ci.toFixed(4)),
    classification,
    description
  });
});

app.listen(PORT, () => {
  console.log(`Loewe Additivity Calculator server running on http://localhost:${PORT}`);
});
