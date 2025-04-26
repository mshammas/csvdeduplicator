import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

function runCsvDeduplicator(args: string[]) {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showErrorMessage('No active editor - open a CSV file first.');
    return;
  }

  const filePath = editor.document.fileName;
  const scriptPath = path.join(__dirname, '..', 'scripts', 'csvdeduplicator.py');
  const command = `python3 "${scriptPath}" ${args.join(' ')} "${filePath}"`;

  const terminal = vscode.window.createTerminal('CSV Deduplicator');
  terminal.sendText(command);
  terminal.show();
}

export function activate(context: vscode.ExtensionContext) {
  // Command: List Headers
  const listHeaders = vscode.commands.registerCommand('csvdeduplicator.listHeaders', async () => {
    runCsvDeduplicator(['-q']);
  });

  // Command: Deduplicate CSV
  const deduplicate = vscode.commands.registerCommand('csvdeduplicator.deduplicate', async () => {
    const rOption = await vscode.window.showInputBox({
      prompt: 'Enter column specifier (-r), or leave blank for all columns'
    });
    let args: string[] = [];
    if (rOption) {
      args.push('-r', rOption);
      const cOption = await vscode.window.showInputBox({
        prompt: 'Enter count of columns (-c), or leave blank'
      });
      if (cOption) {
        args.push('-c', cOption);
      }
    } else {
      const cOption = await vscode.window.showInputBox({
        prompt: 'Enter count of columns (-c), or leave blank for all'
      });
      if (cOption) {
        args.push('-c', cOption);
      }
    }
    runCsvDeduplicator(args);
  });

  context.subscriptions.push(listHeaders, deduplicate);
}

export function deactivate() {}
