#!/usr/bin/env python3
"""
Real-time Collaboration Dashboard
Monitor multi-agent development progress in real-time
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import threading
import time
from datetime import datetime
import os
from agent_communication import comm_hub

class CollaborationDashboard:
    """Real-time dashboard for monitoring collaborative development"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Collaborative CrewAI Development Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Data storage
        self.agent_status = {}
        self.communications = []
        self.file_locks = {}
        self.integration_points = []
        self.file_lock_requests = []
        self.conflict_reports = []
        self.shared_context = {}

        # Statistics tracking
        self.stats = {
            'session_start': datetime.now(),
            'total_messages': 0,
            'files_created': 0,
            'files_modified': 0,
            'lock_requests': 0,
            'lock_approvals': 0,
            'lock_denials': 0,
            'conflicts_resolved': 0,
            'agent_activity': {},
            'hourly_activity': [],
            'performance_metrics': {}
        }
        
        # Create UI
        self.create_widgets()
        
        # Start monitoring thread
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_collaboration, daemon=True)
        self.monitor_thread.start()
        
        # Update UI periodically
        self.update_ui()
    
    def configure_styles(self):
        """Configure dark theme styles"""
        self.style.configure('Title.TLabel', 
                           background='#1e1e1e', 
                           foreground='#ffffff', 
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Header.TLabel', 
                           background='#2d2d2d', 
                           foreground='#ffffff', 
                           font=('Arial', 12, 'bold'))
        
        self.style.configure('Status.TLabel', 
                           background='#1e1e1e', 
                           foreground='#00ff00', 
                           font=('Arial', 10))
        
        self.style.configure('Dark.TFrame', 
                           background='#2d2d2d', 
                           relief='raised')
    
    def create_widgets(self):
        """Create enhanced dashboard widgets"""

        # Main title with session info
        title_frame = ttk.Frame(self.root, style='Dark.TFrame')
        title_frame.pack(fill='x', pady=5)

        title_label = ttk.Label(title_frame,
                               text="🤖 Collaborative CrewAI Development Dashboard",
                               style='Title.TLabel')
        title_label.pack()

        self.session_label = ttk.Label(title_frame,
                                      text=f"Session Started: {self.stats['session_start'].strftime('%Y-%m-%d %H:%M:%S')}",
                                      style='Status.TLabel')
        self.session_label.pack()

        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Tab 1: Overview
        self.create_overview_tab()

        # Tab 2: Statistics
        self.create_statistics_tab()

        # Tab 3: Performance
        self.create_performance_tab()

        # Tab 4: File System
        self.create_filesystem_tab()

        # Status bar
        self.status_bar = ttk.Label(self.root, text="🔄 Monitoring collaborative development...", style='Status.TLabel')
        self.status_bar.pack(side='bottom', fill='x', pady=2)

    def create_overview_tab(self):
        """Create overview tab with main monitoring"""
        overview_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(overview_frame, text="📊 Overview")

        # Create main container
        main_frame = ttk.Frame(overview_frame, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left panel - Agent Status
        left_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=5)

        ttk.Label(left_frame, text="👥 Agent Status", style='Header.TLabel').pack(pady=5)

        self.agent_status_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        self.agent_status_frame.pack(fill='both', expand=True, pady=5)

        # Right panel - Communications
        right_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=5)

        ttk.Label(right_frame, text="💬 Team Communications", style='Header.TLabel').pack(pady=5)

        self.comm_text = scrolledtext.ScrolledText(right_frame,
                                                  height=15,
                                                  bg='#1e1e1e',
                                                  fg='#ffffff',
                                                  font=('Consolas', 9))
        self.comm_text.pack(fill='both', expand=True, pady=5)

        # Bottom panel - File Status and Integration
        bottom_frame = ttk.Frame(overview_frame, style='Dark.TFrame')
        bottom_frame.pack(fill='x', padx=10, pady=5)

        # File locks section
        file_frame = ttk.Frame(bottom_frame, style='Dark.TFrame')
        file_frame.pack(side='left', fill='both', expand=True, padx=5)

        ttk.Label(file_frame, text="🔒 File Locks", style='Header.TLabel').pack()
        self.file_locks_text = tk.Text(file_frame, height=6, bg='#1e1e1e', fg='#ffff00', font=('Consolas', 8))
        self.file_locks_text.pack(fill='both', expand=True)

        # Integration points section
        integration_frame = ttk.Frame(bottom_frame, style='Dark.TFrame')
        integration_frame.pack(side='right', fill='both', expand=True, padx=5)

        ttk.Label(integration_frame, text="🔗 Integration Points", style='Header.TLabel').pack()
        self.integration_text = tk.Text(integration_frame, height=6, bg='#1e1e1e', fg='#00ffff', font=('Consolas', 8))
        self.integration_text.pack(fill='both', expand=True)

    def create_statistics_tab(self):
        """Create statistics tab with detailed metrics"""
        stats_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(stats_frame, text="📈 Statistics")

        # Create scrollable frame
        canvas = tk.Canvas(stats_frame, bg='#1e1e1e')
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Session Overview
        session_frame = ttk.LabelFrame(scrollable_frame, text="📊 Session Overview", style='Dark.TFrame')
        session_frame.pack(fill='x', padx=10, pady=5)

        self.session_stats_frame = ttk.Frame(session_frame, style='Dark.TFrame')
        self.session_stats_frame.pack(fill='x', padx=5, pady=5)

        # Agent Activity
        activity_frame = ttk.LabelFrame(scrollable_frame, text="🤖 Agent Activity", style='Dark.TFrame')
        activity_frame.pack(fill='x', padx=10, pady=5)

        self.activity_stats_frame = ttk.Frame(activity_frame, style='Dark.TFrame')
        self.activity_stats_frame.pack(fill='x', padx=5, pady=5)

        # File Operations
        file_ops_frame = ttk.LabelFrame(scrollable_frame, text="📁 File Operations", style='Dark.TFrame')
        file_ops_frame.pack(fill='x', padx=10, pady=5)

        self.file_ops_stats_frame = ttk.Frame(file_ops_frame, style='Dark.TFrame')
        self.file_ops_stats_frame.pack(fill='x', padx=5, pady=5)

        # Communication Stats
        comm_stats_frame = ttk.LabelFrame(scrollable_frame, text="💬 Communication Stats", style='Dark.TFrame')
        comm_stats_frame.pack(fill='x', padx=10, pady=5)

        self.comm_stats_frame = ttk.Frame(comm_stats_frame, style='Dark.TFrame')
        self.comm_stats_frame.pack(fill='x', padx=5, pady=5)

    def create_performance_tab(self):
        """Create performance monitoring tab"""
        perf_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(perf_frame, text="⚡ Performance")

        # Real-time metrics
        metrics_frame = ttk.LabelFrame(perf_frame, text="📊 Real-time Metrics", style='Dark.TFrame')
        metrics_frame.pack(fill='x', padx=10, pady=5)

        self.metrics_frame = ttk.Frame(metrics_frame, style='Dark.TFrame')
        self.metrics_frame.pack(fill='x', padx=5, pady=5)

        # Performance graphs placeholder
        graph_frame = ttk.LabelFrame(perf_frame, text="📈 Activity Timeline", style='Dark.TFrame')
        graph_frame.pack(fill='both', expand=True, padx=10, pady=5)

        self.timeline_text = scrolledtext.ScrolledText(graph_frame,
                                                      height=20,
                                                      bg='#1e1e1e',
                                                      fg='#00ff00',
                                                      font=('Consolas', 9))
        self.timeline_text.pack(fill='both', expand=True, pady=5)

        # System health
        health_frame = ttk.LabelFrame(perf_frame, text="🏥 System Health", style='Dark.TFrame')
        health_frame.pack(fill='x', padx=10, pady=5)

        self.health_frame = ttk.Frame(health_frame, style='Dark.TFrame')
        self.health_frame.pack(fill='x', padx=5, pady=5)

    def create_filesystem_tab(self):
        """Create filesystem monitoring tab"""
        fs_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(fs_frame, text="📁 File System")

        # File tree
        tree_frame = ttk.LabelFrame(fs_frame, text="🌳 Project Structure", style='Dark.TFrame')
        tree_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.file_tree = ttk.Treeview(tree_frame, style='Dark.TFrame')
        self.file_tree.pack(fill='both', expand=True, pady=5)

        # File details
        details_frame = ttk.LabelFrame(fs_frame, text="📄 File Details", style='Dark.TFrame')
        details_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)

        self.file_details_text = scrolledtext.ScrolledText(details_frame,
                                                          height=25,
                                                          bg='#1e1e1e',
                                                          fg='#ffffff',
                                                          font=('Consolas', 9))
        self.file_details_text.pack(fill='both', expand=True, pady=5)

        # Lock requests
        lock_req_frame = ttk.LabelFrame(fs_frame, text="🔐 Lock Requests", style='Dark.TFrame')
        lock_req_frame.pack(fill='x', padx=5, pady=5)

        self.lock_requests_text = tk.Text(lock_req_frame, height=8, bg='#1e1e1e', fg='#ff9900', font=('Consolas', 8))
        self.lock_requests_text.pack(fill='x', pady=5)
    
    def monitor_collaboration(self):
        """Monitor collaboration data in background thread with enhanced statistics"""
        while self.monitoring:
            try:
                # Check if communication file exists
                if os.path.exists(comm_hub.communication_file):
                    # FIX: Use comm_hub.lock to prevent race conditions when reading JSON file
                    with comm_hub.lock:
                        data = comm_hub._read_data()

                    # Update all data
                    old_comm_count = len(self.communications)
                    self.communications = data.get("communications", [])
                    self.file_locks = data.get("file_locks", {})
                    self.integration_points = data.get("integration_points", [])
                    self.file_lock_requests = data.get("file_lock_requests", [])
                    self.conflict_reports = data.get("conflict_reports", [])
                    self.shared_context = data.get("shared_context", {})

                    # Update statistics
                    self.update_statistics(data, old_comm_count)

                    # Update agent status from status updates
                    status_updates = data.get("status_updates", [])
                    self.agent_status = {}
                    for update in status_updates:
                        agent = update["agent"]
                        self.agent_status[agent] = {
                            "status": update["status"],
                            "timestamp": update["timestamp"],
                            "details": update.get("details", {})
                        }

                        # Track agent activity
                        if agent not in self.stats['agent_activity']:
                            self.stats['agent_activity'][agent] = {
                                'messages_sent': 0,
                                'files_created': 0,
                                'files_modified': 0,
                                'last_activity': update["timestamp"]
                            }

                time.sleep(2)  # Update every 2 seconds

            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(5)

    def update_statistics(self, data, old_comm_count):
        """Update comprehensive statistics"""
        # Message statistics
        new_messages = len(self.communications) - old_comm_count
        self.stats['total_messages'] = len(self.communications)

        # Count different message types
        for comm in self.communications[old_comm_count:]:
            msg_type = comm.get('type', 'unknown')
            agent = comm.get('from_agent', 'unknown')

            # Update agent activity
            if agent in self.stats['agent_activity']:
                self.stats['agent_activity'][agent]['messages_sent'] += 1
                self.stats['agent_activity'][agent]['last_activity'] = comm.get('timestamp', '')

        # File operation statistics
        self.stats['lock_requests'] = len(self.file_lock_requests)
        self.stats['lock_approvals'] = len([r for r in self.file_lock_requests if r.get('status') == 'approved'])
        self.stats['lock_denials'] = len([r for r in self.file_lock_requests if r.get('status') == 'denied'])

        # File system statistics
        self.update_file_system_stats()

        # Performance metrics
        current_time = datetime.now()
        session_duration = current_time - self.stats['session_start']
        self.stats['performance_metrics'] = {
            'session_duration': str(session_duration).split('.')[0],
            'messages_per_minute': round(self.stats['total_messages'] / max(session_duration.total_seconds() / 60, 1), 2),
            'active_agents': len(self.agent_status),
            'avg_response_time': self.calculate_avg_response_time()
        }

        # Add to hourly activity
        hour_key = current_time.strftime('%H:00')
        if not self.stats['hourly_activity'] or self.stats['hourly_activity'][-1]['hour'] != hour_key:
            self.stats['hourly_activity'].append({
                'hour': hour_key,
                'messages': new_messages,
                'agents_active': len(self.agent_status)
            })
        else:
            self.stats['hourly_activity'][-1]['messages'] += new_messages
            self.stats['hourly_activity'][-1]['agents_active'] = max(
                self.stats['hourly_activity'][-1]['agents_active'],
                len(self.agent_status)
            )

    def update_file_system_stats(self):
        """Update file system statistics"""
        try:
            game_dir = "Game"
            if os.path.exists(game_dir):
                total_files = 0
                total_size = 0
                for root, dirs, files in os.walk(game_dir):
                    for file in files:
                        if file.endswith(('.py', '.json', '.md', '.txt')):
                            file_path = os.path.join(root, file)
                            total_files += 1
                            total_size += os.path.getsize(file_path)

                self.stats['files_created'] = total_files
                self.stats['total_project_size'] = total_size
        except Exception as e:
            print(f"File system stats error: {e}")

    def calculate_avg_response_time(self):
        """Calculate average response time between messages"""
        if len(self.communications) < 2:
            return 0

        try:
            times = []
            for i in range(1, min(len(self.communications), 10)):  # Last 10 messages
                curr_time = datetime.fromisoformat(self.communications[i]['timestamp'])
                prev_time = datetime.fromisoformat(self.communications[i-1]['timestamp'])
                times.append((curr_time - prev_time).total_seconds())

            return round(sum(times) / len(times), 2) if times else 0
        except:
            return 0
    
    def update_ui(self):
        """Update UI with latest data across all tabs"""
        try:
            # Update Overview tab
            self.update_agent_status()
            self.update_communications()
            self.update_file_locks()
            self.update_integration_points()

            # Update Statistics tab
            self.update_statistics_display()

            # Update Performance tab
            self.update_performance_display()

            # Update File System tab
            self.update_filesystem_display()

            # Update status bar with comprehensive info
            active_agents = len(self.agent_status)
            recent_comms = len([c for c in self.communications if self.is_recent(c.get("timestamp", ""))])
            session_time = str(datetime.now() - self.stats['session_start']).split('.')[0]

            status_text = (f"🔄 Active: {active_agents} agents | "
                          f"📨 Messages: {self.stats['total_messages']} | "
                          f"🔒 Locks: {len(self.file_locks)} | "
                          f"⏱️ Session: {session_time} | "
                          f"🔄 Updated: {datetime.now().strftime('%H:%M:%S')}")

            self.status_bar.config(text=status_text)

        except Exception as e:
            print(f"UI update error: {e}")

        # Schedule next update
        self.root.after(3000, self.update_ui)  # Update every 3 seconds

    def update_statistics_display(self):
        """Update statistics tab display"""
        try:
            # Session Overview
            for widget in self.session_stats_frame.winfo_children():
                widget.destroy()

            session_stats = [
                ("📅 Session Duration", self.stats['performance_metrics'].get('session_duration', '0:00:00')),
                ("📨 Total Messages", str(self.stats['total_messages'])),
                ("📁 Files Created", str(self.stats['files_created'])),
                ("🔒 Lock Requests", str(self.stats['lock_requests'])),
                ("✅ Approvals", str(self.stats['lock_approvals'])),
                ("❌ Denials", str(self.stats['lock_denials'])),
                ("⚡ Msg/Min", str(self.stats['performance_metrics'].get('messages_per_minute', 0))),
                ("🤖 Active Agents", str(self.stats['performance_metrics'].get('active_agents', 0)))
            ]

            for i, (label, value) in enumerate(session_stats):
                row = i // 4
                col = i % 4
                stat_frame = ttk.Frame(self.session_stats_frame, style='Dark.TFrame')
                stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky='w')

                ttk.Label(stat_frame, text=label, style='Header.TLabel').pack()
                ttk.Label(stat_frame, text=value, style='Status.TLabel', font=('Arial', 12, 'bold')).pack()

            # Agent Activity
            for widget in self.activity_stats_frame.winfo_children():
                widget.destroy()

            for agent, activity in self.stats['agent_activity'].items():
                agent_frame = ttk.Frame(self.activity_stats_frame, style='Dark.TFrame', relief='ridge')
                agent_frame.pack(fill='x', pady=2)

                ttk.Label(agent_frame, text=f"🤖 {agent}", style='Header.TLabel').pack(side='left')
                ttk.Label(agent_frame, text=f"📨 {activity['messages_sent']}", style='Status.TLabel').pack(side='right')
                ttk.Label(agent_frame, text=f"📁 {activity['files_created']}", style='Status.TLabel').pack(side='right')

        except Exception as e:
            print(f"Statistics display error: {e}")

    def update_performance_display(self):
        """Update performance tab display"""
        try:
            # Real-time metrics
            for widget in self.metrics_frame.winfo_children():
                widget.destroy()

            metrics = [
                ("⚡ Avg Response Time", f"{self.stats['performance_metrics'].get('avg_response_time', 0)}s"),
                ("🔄 Update Frequency", "3s"),
                ("💾 Memory Usage", f"{len(str(self.communications)) / 1024:.1f}KB"),
                ("🌐 Network Status", "Connected" if self.communications else "Waiting")
            ]

            for i, (label, value) in enumerate(metrics):
                metric_frame = ttk.Frame(self.metrics_frame, style='Dark.TFrame')
                metric_frame.grid(row=i//2, column=i%2, padx=20, pady=10, sticky='w')

                ttk.Label(metric_frame, text=label, style='Header.TLabel').pack()
                ttk.Label(metric_frame, text=value, style='Status.TLabel', font=('Arial', 14, 'bold')).pack()

            # Activity timeline
            self.timeline_text.delete(1.0, tk.END)
            timeline_data = []

            for comm in self.communications[-20:]:  # Last 20 messages
                timestamp = comm.get('timestamp', '')
                agent = comm.get('from_agent', 'Unknown')
                msg_type = comm.get('type', 'info')
                message = comm.get('message', '')[:50] + '...' if len(comm.get('message', '')) > 50 else comm.get('message', '')

                timeline_data.append(f"[{timestamp[11:19]}] {agent} ({msg_type}): {message}")

            self.timeline_text.insert(tk.END, '\n'.join(timeline_data))
            self.timeline_text.see(tk.END)

        except Exception as e:
            print(f"Performance display error: {e}")

    def update_filesystem_display(self):
        """Update filesystem tab display"""
        try:
            # Update file tree
            self.file_tree.delete(*self.file_tree.get_children())

            if os.path.exists("Game"):
                game_node = self.file_tree.insert("", "end", text="Game", open=True)
                self.populate_file_tree("Game", game_node)

            # Update file details
            self.file_details_text.delete(1.0, tk.END)

            details = []
            details.append("📊 PROJECT STATISTICS")
            details.append("=" * 50)
            details.append(f"📁 Total Files: {self.stats.get('files_created', 0)}")
            details.append(f"💾 Project Size: {self.stats.get('total_project_size', 0)} bytes")
            details.append(f"🔒 Active Locks: {len(self.file_locks)}")
            details.append(f"📋 Pending Requests: {len([r for r in self.file_lock_requests if r.get('status') == 'pending'])}")
            details.append("")

            details.append("🔐 ACTIVE FILE LOCKS")
            details.append("=" * 50)
            for file_path, lock_info in self.file_locks.items():
                details.append(f"📄 {file_path}")
                details.append(f"   🤖 Agent: {lock_info.get('agent', 'Unknown')}")
                details.append(f"   ⏰ Since: {lock_info.get('timestamp', 'Unknown')}")
                details.append("")

            self.file_details_text.insert(tk.END, '\n'.join(details))

            # Update lock requests
            self.lock_requests_text.delete(1.0, tk.END)

            pending_requests = [r for r in self.file_lock_requests if r.get('status') == 'pending']
            if pending_requests:
                for req in pending_requests:
                    req_text = f"🔐 {req.get('agent', 'Unknown')} → {req.get('file_path', 'Unknown')}\n"
                    req_text += f"   ⏰ {req.get('timestamp', 'Unknown')}\n\n"
                    self.lock_requests_text.insert(tk.END, req_text)
            else:
                self.lock_requests_text.insert(tk.END, "✅ No pending lock requests")

        except Exception as e:
            print(f"Filesystem display error: {e}")

    def populate_file_tree(self, path, parent):
        """Populate file tree recursively"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    node = self.file_tree.insert(parent, "end", text=f"📁 {item}", open=False)
                    self.populate_file_tree(item_path, node)
                else:
                    icon = "🐍" if item.endswith('.py') else "📄"
                    self.file_tree.insert(parent, "end", text=f"{icon} {item}")
        except PermissionError:
            pass
    
    def update_agent_status(self):
        """Update agent status display"""
        try:
            # Check if widget exists
            if not hasattr(self, 'agent_status_frame'):
                return

            # Clear existing status widgets
            for widget in self.agent_status_frame.winfo_children():
                widget.destroy()

            if not self.agent_status:
                ttk.Label(self.agent_status_frame, text="⏳ Waiting for agents to start...", style='Status.TLabel').pack()
                return

            for agent, info in self.agent_status.items():
                agent_frame = ttk.Frame(self.agent_status_frame, style='Dark.TFrame', relief='ridge')
                agent_frame.pack(fill='x', pady=2, padx=5)

                # Agent name and status
                status_text = f"🤖 {agent}"
                ttk.Label(agent_frame, text=status_text, style='Header.TLabel').pack(anchor='w')

                status_text = f"Status: {info['status']}"
                ttk.Label(agent_frame, text=status_text, style='Status.TLabel').pack(anchor='w')

                # Timestamp
                try:
                    timestamp = datetime.fromisoformat(info['timestamp']).strftime('%H:%M:%S')
                    time_text = f"Last Update: {timestamp}"
                    ttk.Label(agent_frame, text=time_text, foreground='#888888', background='#2d2d2d').pack(anchor='w')
                except:
                    pass
        except Exception as e:
            print(f"Agent status update error: {e}")
    
    def update_communications(self):
        """Update communications display"""
        try:
            # Check if widget exists
            if not hasattr(self, 'comm_text'):
                return

            self.comm_text.delete(1.0, tk.END)

            # Show recent communications (last 20)
            recent_comms = self.communications[-20:] if len(self.communications) > 20 else self.communications

            for comm in recent_comms:
                try:
                    timestamp = datetime.fromisoformat(comm['timestamp']).strftime('%H:%M:%S')
                    from_agent = comm['from_agent']
                    to_agent = comm['to_agent']
                    message = comm['message']
                    msg_type = comm.get('type', 'info')

                    # Color code by message type
                    if msg_type == 'code_review_request':
                        color = '#ffaa00'  # Orange
                    elif msg_type == 'conflict':
                        color = '#ff4444'  # Red
                    elif msg_type == 'integration_point':
                        color = '#44ff44'  # Green
                    else:
                        color = '#ffffff'  # White

                    comm_line = f"[{timestamp}] {from_agent} → {to_agent}: {message}\n"
                    self.comm_text.insert(tk.END, comm_line)

                except Exception as e:
                    print(f"Communication display error: {e}")

            # Auto-scroll to bottom
            self.comm_text.see(tk.END)
        except Exception as e:
            print(f"Communications update error: {e}")
    
    def update_file_locks(self):
        """Update file locks display"""
        try:
            # Check if widget exists
            if not hasattr(self, 'file_locks_text'):
                return

            self.file_locks_text.delete(1.0, tk.END)

            if not self.file_locks:
                self.file_locks_text.insert(tk.END, "✅ No files currently locked\n")
            else:
                for file_path, lock_info in self.file_locks.items():
                    try:
                        agent = lock_info['agent']
                        timestamp = datetime.fromisoformat(lock_info['timestamp']).strftime('%H:%M:%S')
                        lock_line = f"🔒 {file_path}\n   Locked by: {agent} at {timestamp}\n\n"
                        self.file_locks_text.insert(tk.END, lock_line)
                    except:
                        pass
        except Exception as e:
            print(f"File locks update error: {e}")
    
    def update_integration_points(self):
        """Update integration points display"""
        try:
            # Check if widget exists
            if not hasattr(self, 'integration_text'):
                return

            self.integration_text.delete(1.0, tk.END)

            if not self.integration_points:
                self.integration_text.insert(tk.END, "⏳ No integration points registered yet\n")
            else:
                # Show recent integration points (last 10)
                recent_points = self.integration_points[-10:] if len(self.integration_points) > 10 else self.integration_points

                for point in recent_points:
                    try:
                        timestamp = datetime.fromisoformat(point['timestamp']).strftime('%H:%M:%S')
                        agent = point['agent']
                        component = point['component']
                        point_line = f"🔗 [{timestamp}] {component}\n   by {agent}\n\n"
                        self.integration_text.insert(tk.END, point_line)
                    except:
                        pass
        except Exception as e:
            print(f"Integration points update error: {e}")
    
    def is_recent(self, timestamp_str, minutes=5):
        """Check if timestamp is within recent minutes"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
            now = datetime.now()
            return (now - timestamp).total_seconds() < (minutes * 60)
        except:
            return False
    
    def run(self):
        """Run the dashboard"""
        try:
            self.root.mainloop()
        finally:
            self.monitoring = False

def main():
    """Main function to run the dashboard"""
    print("🚀 Starting Collaborative Development Dashboard...")
    dashboard = CollaborationDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
