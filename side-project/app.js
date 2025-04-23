import React, { useState } from 'react';
import * as XLSX from 'xlsx';

export default function WebsitePrototype() {
  const [data, setData] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [selectedColumn, setSelectedColumn] = useState('');
  const [condition, setCondition] = useState('');
  const [highlightedRows, setHighlightedRows] = useState([]);
  const [onlyShowHighlighted, setOnlyShowHighlighted] = useState(false);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      const bstr = event.target.result;
      const wb = XLSX.read(bstr, { type: 'binary' });
      const wsname = wb.SheetNames[0];
      const ws = wb.Sheets[wsname];
      const jsonData = XLSX.utils.sheet_to_json(ws, { header: 1 });
      setHeaders(jsonData[0]);
      setData(jsonData.slice(1));
    };
    reader.readAsBinaryString(file);
  };

  const applyHighlight = () => {
    const colIndex = headers.indexOf(selectedColumn);
    if (colIndex === -1) return;
    const newHighlightedRows = data.map((row, idx) => {
      const cell = row[colIndex];
      try {
        return eval(`${cell} ${condition}`) ? idx : null;
      } catch {
        return null;
      }
    }).filter(idx => idx !== null);
    setHighlightedRows(newHighlightedRows);
  };

  const displayRows = onlyShowHighlighted
    ? data.filter((_, idx) => highlightedRows.includes(idx))
    : data;

  return (
    <div className="p-4 grid gap-4">
      <header className="text-2xl font-bold">Excel Highlight Tool</header>

      <input type="file" accept=".xlsx, .xls" onChange={handleFileUpload} className="border p-2" />

      {headers.length > 0 && (
        <div className="grid gap-2">
          <div className="flex gap-2">
            <select onChange={e => setSelectedColumn(e.target.value)} className="border p-2">
              <option value="">Select Column</option>
              {headers.map((header, idx) => (
                <option key={idx} value={header}>{header}</option>
              ))}
            </select>
            <input
              type="text"
              placeholder="e.g., > 100"
              value={condition}
              onChange={e => setCondition(e.target.value)}
              className="border p-2"
            />
            <button onClick={applyHighlight} className="bg-blue-500 text-white px-4 py-2 rounded">Highlight</button>
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={onlyShowHighlighted}
                onChange={() => setOnlyShowHighlighted(!onlyShowHighlighted)}
              />
              Show Only Highlighted Rows
            </label>
          </div>

          <table className="table-auto border-collapse w-full">
            <thead>
              <tr>
                {headers.map((header, idx) => (
                  <th key={idx} className="border px-2 py-1 bg-gray-100">{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {displayRows.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, colIndex) => (
                    <td
                      key={colIndex}
                      className={`border px-2 py-1 ${highlightedRows.includes(rowIndex) && headers[colIndex] === selectedColumn ? 'bg-yellow-200' : ''}`}
                    >
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <footer className="text-center text-sm text-gray-500 mt-4">© 2025 Excel Tool</footer>
    </div>
  );
}
