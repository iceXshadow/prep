#!/usr/bin/env python3
"""
Commit Message Generator

This script analyzes git changes and generates appropriate commit messages
based on the type of changes made.

Usage:
    python commit_message_generator.py
    python commit_message_generator.py --staged
    python commit_message_generator.py --help
"""

import subprocess
import re
import argparse
from typing import List, Dict, Tuple
from pathlib import Path


class CommitMessageGenerator:
    def __init__(self):
        self.commit_types = {
            'feat': 'A new feature',
            'fix': 'A bug fix',
            'docs': 'Documentation only changes',
            'style': 'Changes that do not affect the meaning of the code',
            'refactor': 'A code change that neither fixes a bug nor adds a feature',
            'test': 'Adding missing tests or correcting existing tests',
            'chore': 'Changes to the build process or auxiliary tools',
            'perf': 'A code change that improves performance',
            'ci': 'Changes to CI configuration files and scripts',
            'build': 'Changes that affect the build system or external dependencies',
            'revert': 'Reverts a previous commit'
        }
        
        # Keywords that indicate different types of changes
        self.keywords = {
            'feat': [
                'add', 'create', 'implement', 'introduce', 'new', 'feature',
                'support', 'enable', 'allow', 'provide', 'include'
            ],
            'fix': [
                'fix', 'resolve', 'correct', 'repair', 'patch', 'solve',
                'handle', 'prevent', 'avoid', 'address', 'bug', 'issue', 'error'
            ],
            'docs': [
                'readme', 'documentation', 'comment', 'docstring', 'guide',
                'tutorial', 'example', 'doc', 'md', 'rst', 'txt'
            ],
            'style': [
                'format', 'indent', 'whitespace', 'semicolon', 'style',
                'lint', 'prettier', 'formatting', 'spacing'
            ],
            'refactor': [
                'refactor', 'restructure', 'reorganize', 'cleanup', 'simplify',
                'extract', 'move', 'rename', 'split', 'merge', 'optimize'
            ],
            'test': [
                'test', 'spec', 'unittest', 'pytest', 'mock', 'fixture',
                'coverage', 'testing', 'assert'
            ],
            'chore': [
                'update', 'upgrade', 'dependency', 'package', 'config',
                'setup', 'build', 'deploy', 'release', 'version', 'maintenance'
            ],
            'perf': [
                'performance', 'optimize', 'faster', 'speed', 'cache',
                'efficient', 'benchmark', 'memory', 'cpu'
            ],
            'ci': [
                'ci', 'pipeline', 'workflow', 'github', 'jenkins', 'travis',
                'gitlab', 'azure', 'actions', 'deployment'
            ],
            'build': [
                'dockerfile', 'makefile', 'package.json', 'requirements.txt',
                'setup.py', 'cmake', 'gradle', 'npm', 'pip', 'yarn'
            ]
        }

    def run_git_command(self, cmd: List[str]) -> str:
        """Run a git command and return the output."""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                cwd=Path.cwd()
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running git command: {e}")
            return ""
        except FileNotFoundError:
            print("Git is not installed or not in PATH")
            return ""

    def get_git_diff(self, staged: bool = False) -> str:
        """Get git diff output."""
        if staged:
            return self.run_git_command(['git', 'diff', '--staged'])
        else:
            return self.run_git_command(['git', 'diff'])

    def get_git_status(self) -> str:
        """Get git status output."""
        return self.run_git_command(['git', 'status', '--porcelain'])

    def get_changed_files(self, staged: bool = False) -> List[str]:
        """Get list of changed files."""
        status = self.get_git_status()
        if not status:
            return []
        
        files = []
        for line in status.split('\n'):
            if line.strip():
                # Git status format: XY filename
                status_code = line[:2]
                filename = line[3:].strip()
                
                if staged:
                    # For staged changes, look at the first character
                    if status_code[0] != ' ' and status_code[0] != '?':
                        files.append(filename)
                else:
                    # For unstaged changes, look at the second character
                    if status_code[1] != ' ' and status_code[1] != '?':
                        files.append(filename)
                    # Also include untracked files
                    elif status_code == '??':
                        files.append(filename)
        
        return files

    def analyze_file_types(self, files: List[str]) -> Dict[str, int]:
        """Analyze file types and extensions."""
        analysis = {
            'source_files': 0,
            'test_files': 0,
            'doc_files': 0,
            'config_files': 0,
            'build_files': 0,
            'total_files': len(files)
        }
        
        for file in files:
            file_lower = file.lower()
            path = Path(file)
            
            # Test files
            if 'test' in file_lower or 'spec' in file_lower or file_lower.endswith('.test.py'):
                analysis['test_files'] += 1
            # Documentation files
            elif path.suffix in ['.md', '.rst', '.txt'] or 'readme' in file_lower:
                analysis['doc_files'] += 1
            # Configuration files
            elif path.suffix in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
                analysis['config_files'] += 1
            # Build files
            elif path.name in ['Dockerfile', 'Makefile', 'package.json', 'requirements.txt', 'setup.py']:
                analysis['build_files'] += 1
            # Source files
            elif path.suffix in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.css', '.html']:
                analysis['source_files'] += 1
        
        return analysis

    def analyze_diff_content(self, diff: str) -> Dict[str, int]:
        """Analyze the content of the diff."""
        analysis = {
            'additions': 0,
            'deletions': 0,
            'function_additions': 0,
            'class_additions': 0,
            'import_changes': 0,
            'comment_changes': 0,
            'test_changes': 0
        }
        
        lines = diff.split('\n')
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                analysis['additions'] += 1
                line_content = line[1:].strip().lower()
                
                # Check for function definitions
                if line_content.startswith('def ') or 'function' in line_content:
                    analysis['function_additions'] += 1
                
                # Check for class definitions
                if line_content.startswith('class '):
                    analysis['class_additions'] += 1
                
                # Check for imports
                if line_content.startswith('import ') or line_content.startswith('from '):
                    analysis['import_changes'] += 1
                
                # Check for comments
                if line_content.startswith('#') or line_content.startswith('//') or line_content.startswith('/*'):
                    analysis['comment_changes'] += 1
                
                # Check for test-related content
                if 'test' in line_content or 'assert' in line_content:
                    analysis['test_changes'] += 1
                    
            elif line.startswith('-') and not line.startswith('---'):
                analysis['deletions'] += 1
        
        return analysis

    def determine_commit_type(self, files: List[str], diff: str) -> str:
        """Determine the most appropriate commit type."""
        if not files:
            return 'chore'
        
        file_analysis = self.analyze_file_types(files)
        diff_analysis = self.analyze_diff_content(diff)
        
        # Score each commit type
        scores = {commit_type: 0 for commit_type in self.commit_types.keys()}
        
        # Analyze based on file types
        if file_analysis['test_files'] > 0:
            scores['test'] += 3
        
        if file_analysis['doc_files'] > 0:
            scores['docs'] += 3
        
        if file_analysis['config_files'] > 0 or file_analysis['build_files'] > 0:
            scores['chore'] += 2
        
        # Analyze based on diff content
        if diff_analysis['function_additions'] > 0 or diff_analysis['class_additions'] > 0:
            scores['feat'] += 2
        
        if diff_analysis['test_changes'] > 0:
            scores['test'] += 2
        
        if diff_analysis['comment_changes'] > 0:
            scores['docs'] += 1
        
        # Analyze based on keywords in file names and diff
        content_to_analyze = ' '.join(files) + ' ' + diff
        content_lower = content_to_analyze.lower()
        
        for commit_type, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    scores[commit_type] += 1
        
        # If no clear winner, default based on file changes
        if max(scores.values()) == 0:
            if file_analysis['source_files'] > 0:
                return 'feat'
            else:
                return 'chore'
        
        # Return the commit type with the highest score
        return max(scores, key=scores.get)

    def generate_commit_message(self, files: List[str], diff: str) -> str:
        """Generate a commit message based on the changes."""
        if not files:
            return "chore: no changes detected"
        
        commit_type = self.determine_commit_type(files, diff)
        file_analysis = self.analyze_file_types(files)
        diff_analysis = self.analyze_diff_content(diff)
        
        # Generate the main message
        if commit_type == 'feat':
            if diff_analysis['function_additions'] > 0:
                message = "add new functionality"
            elif diff_analysis['class_additions'] > 0:
                message = "add new classes"
            else:
                message = "add new features"
        
        elif commit_type == 'fix':
            message = "fix issues and bugs"
        
        elif commit_type == 'docs':
            if file_analysis['doc_files'] > 0:
                message = "update documentation"
            else:
                message = "add comments and documentation"
        
        elif commit_type == 'test':
            message = "add/update tests"
        
        elif commit_type == 'refactor':
            message = "refactor code structure"
        
        elif commit_type == 'style':
            message = "format code and fix style issues"
        
        elif commit_type == 'chore':
            if file_analysis['config_files'] > 0:
                message = "update configuration"
            elif file_analysis['build_files'] > 0:
                message = "update build files"
            else:
                message = "update dependencies and maintenance"
        
        elif commit_type == 'perf':
            message = "improve performance"
        
        elif commit_type == 'ci':
            message = "update CI/CD configuration"
        
        elif commit_type == 'build':
            message = "update build system"
        
        else:
            message = "make various changes"
        
        # Add file context if helpful
        if len(files) == 1:
            file_name = Path(files[0]).name
            message += f" in {file_name}"
        elif len(files) <= 3:
            file_names = [Path(f).name for f in files]
            message += f" in {', '.join(file_names)}"
        elif file_analysis['total_files'] > 3:
            message += f" across {file_analysis['total_files']} files"
        
        return f"{commit_type}: {message}"

    def generate_detailed_message(self, files: List[str], diff: str) -> str:
        """Generate a detailed commit message with body."""
        main_message = self.generate_commit_message(files, diff)
        
        file_analysis = self.analyze_file_types(files)
        diff_analysis = self.analyze_diff_content(diff)
        
        details = []
        
        if diff_analysis['additions'] > 0:
            details.append(f"- Added {diff_analysis['additions']} lines")
        
        if diff_analysis['deletions'] > 0:
            details.append(f"- Removed {diff_analysis['deletions']} lines")
        
        if diff_analysis['function_additions'] > 0:
            details.append(f"- Added {diff_analysis['function_additions']} new functions")
        
        if diff_analysis['class_additions'] > 0:
            details.append(f"- Added {diff_analysis['class_additions']} new classes")
        
        if file_analysis['test_files'] > 0:
            details.append(f"- Modified {file_analysis['test_files']} test files")
        
        if file_analysis['doc_files'] > 0:
            details.append(f"- Updated {file_analysis['doc_files']} documentation files")
        
        if details:
            return f"{main_message}\n\n" + "\n".join(details)
        else:
            return main_message

    def interactive_mode(self, staged: bool = False):
        """Run in interactive mode to let user choose/modify the message."""
        print("🚀 Commit Message Generator")
        print("=" * 40)
        
        files = self.get_changed_files(staged)
        if not files:
            print("No changes detected.")
            return
        
        print(f"Changed files ({len(files)}):")
        for file in files[:10]:  # Show first 10 files
            print(f"  • {file}")
        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more files")
        
        print()
        
        diff = self.get_git_diff(staged)
        suggested_message = self.generate_commit_message(files, diff)
        detailed_message = self.generate_detailed_message(files, diff)
        
        print(f"Suggested commit message:")
        print(f"📝 {suggested_message}")
        print()
        
        print("Available commit types:")
        for commit_type, description in self.commit_types.items():
            print(f"  {commit_type}: {description}")
        print()
        
        while True:
            choice = input("Choose an option:\n"
                          "1. Use suggested message\n"
                          "2. Use detailed message\n"
                          "3. Customize message\n"
                          "4. Change commit type\n"
                          "5. Exit\n"
                          "Enter your choice (1-5): ").strip()
            
            if choice == '1':
                print(f"\n📋 Final message:\n{suggested_message}")
                if input("\nCopy to clipboard? (y/n): ").lower() == 'y':
                    self.copy_to_clipboard(suggested_message)
                break
            
            elif choice == '2':
                print(f"\n📋 Final message:\n{detailed_message}")
                if input("\nCopy to clipboard? (y/n): ").lower() == 'y':
                    self.copy_to_clipboard(detailed_message)
                break
            
            elif choice == '3':
                custom_message = input("Enter your custom message: ").strip()
                if custom_message:
                    print(f"\n📋 Final message:\n{custom_message}")
                    if input("\nCopy to clipboard? (y/n): ").lower() == 'y':
                        self.copy_to_clipboard(custom_message)
                    break
            
            elif choice == '4':
                print("Available types:", ', '.join(self.commit_types.keys()))
                new_type = input("Enter commit type: ").strip()
                if new_type in self.commit_types:
                    message_body = suggested_message.split(': ', 1)[1]
                    new_message = f"{new_type}: {message_body}"
                    print(f"\n📋 Final message:\n{new_message}")
                    if input("\nCopy to clipboard? (y/n): ").lower() == 'y':
                        self.copy_to_clipboard(new_message)
                    break
                else:
                    print("Invalid commit type!")
            
            elif choice == '5':
                print("Goodbye! 👋")
                break
            
            else:
                print("Invalid choice. Please try again.")

    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard."""
        try:
            # Try to use Windows clipboard
            subprocess.run(['clip'], input=text, text=True, check=True)
            print("✅ Copied to clipboard!")
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Try to use macOS clipboard
                subprocess.run(['pbcopy'], input=text, text=True, check=True)
                print("✅ Copied to clipboard!")
            except (subprocess.CalledProcessError, FileNotFoundError):
                try:
                    # Try to use Linux clipboard
                    subprocess.run(['xclip', '-selection', 'clipboard'], input=text, text=True, check=True)
                    print("✅ Copied to clipboard!")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("❌ Could not copy to clipboard. Please copy manually:")
                    print(f"'{text}'")


def main():
    parser = argparse.ArgumentParser(
        description="Generate commit messages based on git changes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python commit_message_generator.py              # Analyze unstaged changes
  python commit_message_generator.py --staged     # Analyze staged changes
  python commit_message_generator.py --quick      # Generate quick message
        """
    )
    
    parser.add_argument(
        '--staged', 
        action='store_true',
        help='Analyze staged changes instead of unstaged changes'
    )
    
    parser.add_argument(
        '--quick', 
        action='store_true',
        help='Generate quick message without interactive mode'
    )
    
    args = parser.parse_args()
    
    generator = CommitMessageGenerator()
    
    if args.quick:
        files = generator.get_changed_files(args.staged)
        if not files:
            print("No changes detected.")
            return
        
        diff = generator.get_git_diff(args.staged)
        message = generator.generate_commit_message(files, diff)
        print(message)
    else:
        generator.interactive_mode(args.staged)


if __name__ == "__main__":
    main()
