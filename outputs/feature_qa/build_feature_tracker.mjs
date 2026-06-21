import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = new URL("./", import.meta.url).pathname;
const workbook = Workbook.create();
const tracker = workbook.worksheets.add("User Stories");
const summary = workbook.worksheets.add("Summary");

const stories = [
  ["US001", "Menu", "As a player, I can press ENTER on the main menu to start a fresh game.", "ENTER from menu starts level 1, resets total score to 0, and creates a gameplay state.", "lib/Core.py:_manejar_menu,_iniciar_juego", "Automated", "Passed", "None", "", "Passed"],
  ["US002", "Menu", "As a player, I can click JUGAR to start a fresh game.", "Clicking the JUGAR button starts level 1 with a new EstadoJuego.", "lib/Core.py:_manejar_menu", "Automated", "Passed", "None", "", "Passed"],
  ["US003", "Credits", "As a player, I can open credits and return to the menu.", "Clicking CREDITOS shows credits; ENTER returns to the menu.", "lib/Core.py:_manejar_menu,_manejar_creditos; Creditos.py", "Automated", "Passed", "None", "", "Passed"],
  ["US004", "Audio", "As a player, I can toggle music with the menu music button.", "Clicking MUSICA switches the music state between ON and OFF.", "lib/Core.py:_manejar_menu; lib/Audio.py", "Automated", "Passed", "None", "", "Passed"],
  ["US005", "Audio", "As a player, I can press M to toggle music from the event loop.", "Pressing M toggles music once via the global event route.", "lib/Core.py:_loop; lib/Audio.py", "Automated", "Passed", "None", "", "Passed"],
  ["US006", "Navigation", "As a player, I can press ESC during gameplay to return to the menu.", "ESC changes gameplay back to menu without altering music state.", "lib/Core.py:_loop", "Automated", "Passed", "None", "", "Passed"],
  ["US007", "Shooting", "As a player, I can hold and release SPACE to fire an arrow.", "SPACE down begins charging; SPACE up creates an active arrow and resets charging.", "lib/Core.py:EstadoJuego.procesar_evento; lib/Entidades.py:Arquero", "Automated", "Passed", "None", "", "Passed"],
  ["US008", "Aiming", "As a player, I can adjust aim with UP and DOWN.", "Angle is adjustable and clamped between -85 and 10 degrees.", "lib/Core.py:EstadoJuego.actualizar; lib/Entidades.py:Arquero.ajustar_angulo", "Automated", "Passed", "None", "", "Passed"],
  ["US009", "Rounds", "As a player, each round gives one correct target and three distractors.", "Round generation creates four targets with exactly one target matching the answer.", "lib/Core.py:EstadoJuego._nueva_ronda; lib/Entidades.py:generar_blancos", "Automated", "Passed", "None", "", "Passed"],
  ["US010", "Math", "As a player, I see arithmetic prompts with correct answer mapping.", "All level generators return answers matching the displayed expression.", "lib/Niveles.py", "Automated", "Passed", "None", "", "Passed"],
  ["US011", "Timer", "As a player, I lose one arrow when a round timer expires.", "Timeout shows feedback, plays failure sound path, removes one arrow, and starts a new round unless out of arrows.", "lib/Core.py:EstadoJuego.actualizar", "Automated", "Passed", "None", "", "Passed"],
  ["US012", "Miss", "As a player, I lose points and one arrow when a shot leaves the screen.", "A missed active arrow subtracts 10 points without going below zero, consumes one arrow, and shows miss feedback.", "lib/Core.py:EstadoJuego.actualizar", "Automated", "Passed", "None", "", "Passed"],
  ["US013", "Scoring", "As a player, I earn points and progress when I hit the correct target.", "Correct hit adds base score plus time bonus, increments aciertos, and shows correct feedback.", "lib/Core.py:EstadoJuego._verificar_colision", "Automated", "Passed", "None", "", "Passed"],
  ["US014", "Scoring", "As a player, I am penalized when I hit an incorrect target.", "Incorrect hit subtracts 30 points without going below zero, consumes one arrow, and shows incorrect feedback.", "lib/Core.py:EstadoJuego._verificar_colision", "Automated", "Passed", "None", "", "Passed"],
  ["US015", "Progression", "As a player, I complete a level after five correct answers.", "The fifth correct hit marks the level complete without defeat.", "lib/Core.py:EstadoJuego._verificar_colision", "Automated", "Passed", "None", "", "Passed"],
  ["US016", "Progression", "As a player, I advance between levels and win after the final level.", "ENTER after a completed non-final level starts the next level preserving score; final completion enters victory.", "lib/Core.py:_manejar_transicion,_actualizar", "Automated", "Passed", "None", "", "Passed"],
  ["US017", "Game Over", "As a player, I can return to a fresh menu state after game over.", "ENTER from game over returns to menu and resets level, score, and active game state.", "lib/Core.py:_manejar_transicion", "Automated", "Passed", "None", "", "Passed"],
  ["US018", "Assets", "As a player, I see the expected backgrounds and sprites.", "All level backgrounds and core sprites load successfully and can be scaled/rendered.", "lib/Assets.py; Sprite/*", "Automated", "Passed", "None", "", "Passed"],
  ["US019", "Rendering", "As a player, all main screens can render without crashing.", "Gameplay, credits, game over, and victory draw methods complete after normal startup initialization.", "lib/Core.py:_dibujar; Creditos.py", "Automated", "Harness setup failed until fonts were initialized like Core.iniciar()", "Test harness initially bypassed _init_fuentes, causing KeyError('enunciado'). App startup path already initializes fonts.", "Adjusted test setup to initialize fonts before direct draw smoke checks.", "Passed"],
  ["US020", "Menu UX", "As a player, the menu instructions accurately describe how to start.", "Menu copy should not imply that any click starts the game; it should identify ENTER or the JUGAR button.", "lib/Core.py:_dibujar_menu", "Code review", "Failed", "Menu text said 'ENTER o clic para continuar' even though only JUGAR click starts gameplay.", "Changed copy to 'ENTER o clic en JUGAR para empezar'.", "Passed"],
];

const headers = ["ID", "Feature", "User Story", "Expected Behavior", "Source", "Test Method", "Initial Status", "Error / Observation", "Fix Applied", "Post-Fix Status"];
tracker.getRangeByIndexes(0, 0, 1, headers.length).values = [headers];
tracker.getRangeByIndexes(1, 0, stories.length, headers.length).values = stories;

tracker.showGridLines = false;
tracker.freezePanes.freezeRows(1);
tracker.getRange("A1:J1").format.fill = { color: "#1F4E79" };
tracker.getRange("A1:J1").format.font = { color: "#FFFFFF", bold: true };
tracker.getRange("A1:J21").format.borders = { preset: "inside", style: "thin", color: "#D9E2F3" };
tracker.getRange("A1:J21").format.borders = { preset: "outside", style: "medium", color: "#9EADCC" };
tracker.getRange("A:J").format.wrapText = true;
tracker.getRange("A:A").format.columnWidth = 10;
tracker.getRange("B:B").format.columnWidth = 16;
tracker.getRange("C:C").format.columnWidth = 46;
tracker.getRange("D:D").format.columnWidth = 54;
tracker.getRange("E:E").format.columnWidth = 42;
tracker.getRange("F:F").format.columnWidth = 16;
tracker.getRange("G:G").format.columnWidth = 18;
tracker.getRange("H:H").format.columnWidth = 50;
tracker.getRange("I:I").format.columnWidth = 42;
tracker.getRange("J:J").format.columnWidth = 18;
tracker.getRange("A2:B21").format.font = { bold: true };
tracker.getRange("A2:J21").format.verticalAlignment = "top";

const statuses = stories.map((row) => row[9]);
const passed = statuses.filter((status) => status === "Passed").length;
const fixed = stories.filter((row) => row[8]).length;
const automated = stories.filter((row) => row[5] === "Automated").length;

summary.showGridLines = false;
summary.getRange("A1:D1").merge();
summary.getRange("A1").values = [["Flechas y Cuentas - Feature QA Tracker"]];
summary.getRange("A1").format.fill = { color: "#1F4E79" };
summary.getRange("A1").format.font = { color: "#FFFFFF", bold: true, size: 16 };
summary.getRange("A3:B7").values = [
  ["Total user stories", stories.length],
  ["Automated checks", automated],
  ["Stories fixed or test-adjusted", fixed],
  ["Post-fix passed", passed],
  ["Canonical test command", "python3 -m unittest tests.test_user_stories -v"],
];
summary.getRange("A3:A7").format.font = { bold: true };
summary.getRange("A3:B7").format.borders = { preset: "all", style: "thin", color: "#D9E2F3" };
summary.getRange("A3:A7").format.fill = { color: "#EAF2F8" };
summary.getRange("A:B").format.columnWidth = 34;
summary.getRange("B:B").format.columnWidth = 62;
summary.getRange("A9:D9").merge();
summary.getRange("A9").values = [["Notes"]];
summary.getRange("A9").format.fill = { color: "#EAF2F8" };
summary.getRange("A9").format.font = { bold: true };
summary.getRange("A10:D13").merge();
summary.getRange("A10").values = [["Initial testing found one real UX text issue in the main menu and one test harness setup issue while directly invoking draw methods. After the menu copy fix and harness correction, all tracked stories passed retesting."]];
summary.getRange("A10").format.wrapText = true;
summary.getRange("A10:D13").format.borders = { preset: "outside", style: "thin", color: "#D9E2F3" };

const storyInspect = await workbook.inspect({
  kind: "table",
  sheetId: "User Stories",
  range: "A1:J21",
  tableMaxRows: 6,
  tableMaxCols: 10,
  maxChars: 5000,
});
console.log(storyInspect.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

for (const sheetName of ["Summary", "User Stories"]) {
  const blob = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const bytes = new Uint8Array(await blob.arrayBuffer());
  await fs.writeFile(`${outputDir}/preview_${sheetName.replaceAll(" ", "_")}.png`, bytes);
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(`${outputDir}/feature_user_story_tracker.xlsx`);
