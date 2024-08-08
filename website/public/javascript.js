let csvData = [];

async function fillCSV() {
  await fetchAndParseCSV("output2.csv");
}

async function fetchAndParseCSV(filePath) {
  try {
    const response = await fetch(filePath);
    const text = await response.text();
    const rows = text.trim().split("\n");
    csvData = rows.map((row) => row.split(","));
  } catch (error) {
    console.error("Error fetching or parsing CSV file:", error);
  }
}

fillCSV();

document
  .getElementById("dataForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    // Get form values
    const RefSeq = document.getElementById("RefSeq").value;
    const EditedSeq = document.getElementById("EditedSeq").value;
    const PEsystem = document.getElementById("PEsystem").value;
    const EditType = document.getElementById("EditType").value;
    const EditLength = document.getElementById("EditLength").value;
    const MaximumRTTLength = document.getElementById("MaximumRTTLength").value;
    const MaximumPBSLength = document.getElementById("MaximumPBSLength").value;

    if (RefSeq && EditedSeq && EditType) {
      // Run the encodeSequences function
      const encodedMatrix = encodeSequences(RefSeq, EditedSeq);
      displayEncodedMatrix(encodedMatrix);

      compareAndDisplayResultsInResultTable(RefSeq, EditedSeq, EditType);
    }

    function displayEncodedMatrix(matrix) {
      const container = document.getElementById("encodedMatrixContainer");
      const table = document.getElementById("encodedMatrixTable");
      table.innerHTML = ""; // Clear previous data

      matrix.forEach((row) => {
        const tableRow = document.createElement("tr");
        row.forEach((cell) => {
          const tableCell = document.createElement("td");
          tableCell.innerText = cell;
          if (cell === 1) {
            tableCell.classList.add("bg-1");
          } else if (cell === 0) {
            tableCell.classList.add("bg-0");
          } else if (cell === -1) {
            tableCell.classList.add("bg-minus-1");
          }
          tableRow.appendChild(tableCell);
        });
        table.appendChild(tableRow);
      });

      container.style.display = "block"; // Show the container
    }

    function compareAndDisplayResultsInResultTable(
      RefSeq,
      EditedSeq,
      EditType
    ) {
      const table = document.getElementById("dataTable");
      table.innerHTML = ""; // Clear previous data

      csvData.forEach((row, index) => {
        if (index !== 0) {
          const originalSeq = row[0];
          const editedSeq = row[1];
          const mutationType = row[2];
          if (
            RefSeq === originalSeq &&
            EditedSeq === editedSeq &&
            EditType === mutationType
          ) {
            const tableRow = table.insertRow();
            const newRow = row.slice(3, row.length);

            newRow.forEach((cell, cellIndex) => {
              const tableCell = document.createElement("td");
              tableCell.innerText = cell;
              tableRow.appendChild(tableCell);
            });
          }
        }
      });

      const resultHeader = document.querySelector(".result-header");
      const resultTable = document.querySelector(".result-table");
      resultHeader.style.display = "block";
      resultTable.style.display = "table";
    }
  });

// -------- Algorithm --------
function initializeMatrix(rows, columns) {
  const matrix = [];
  for (let i = 0; i < rows; i++) {
    matrix.push(new Array(columns).fill(0));
  }
  return matrix;
}

function encodeSequences(dnaSeq, pegRNASeq) {
  const length = dnaSeq.length;
  const matrix = initializeMatrix(8, length);

  for (let x = 0; x < length; x++) {
    const dnaNuc = dnaSeq[x];
    const pegRNANuc = pegRNASeq[x];

    // Rules 1-3: Update the first four rows based on the existence of nucleotides
    if (dnaNuc === pegRNANuc) {
      matrix[0][x] = -1;
      matrix[1][x] = -1;
      matrix[2][x] = -1;
      matrix[3][x] = -1;
    } else {
      matrix[0][x] = 1;
      matrix[1][x] = 1;
      matrix[2][x] = 1;
      matrix[3][x] = 1;
    }

    // Rule 4: Encode the matching of the two sequences in one position
    if (dnaNuc === pegRNANuc) {
      matrix[4][x] = 1;
      matrix[5][x] = 1;
    }

    // Rules 5-6: Encode the existence of a gap in any of the two sequences
    if (dnaNuc !== "-" && pegRNANuc === "-") {
      matrix[4][x] = 1;
    } else if (dnaNuc === "-" && pegRNANuc !== "-") {
      matrix[5][x] = 1;
    }

    // Rule 7: Mismatches between the two sequences
    if (dnaNuc !== pegRNANuc) {
      matrix[6][x] = 1;
    }

    // Rule 8: PAM sequence
    if (x >= length - 3) {
      // Assuming PAM is the last 3 positions of PegRNA
      matrix[7][x] = 1;
    }
  }

  return matrix;
}
