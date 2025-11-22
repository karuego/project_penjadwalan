const std = @import("std");

pub fn main() !void {
    var gpa = std.heap.DebugAllocator(.{}){};
    defer _ = gpa.deinit();

    const allocator = gpa.allocator();

    const myapp = &[_][]const u8{
        "uv",
        "run",
        "/home/kae/Studio/Git/karuego/project_penjadwalan/src/myapp/main.py",
    };

    //try std.process.changeCurDir("/home/kae/Studio/Git/karuego/project_penjadwalan");
    var child_process = std.process.Child.init(myapp, allocator);
    child_process.cwd = "/home/kae/Studio/Git/karuego/project_penjadwalan";
    try child_process.spawn();
    const status = try child_process.wait();
    switch (status) {
        .Exited => |code| {
            std.debug.print("Process exited normally with code {d}", .{code});
        },
        .Signal => |code| {
            std.debug.print("Process was terminated with signal {d}", .{code});
        },
        .Stopped => |code| {
            std.debug.print("Process was stopped (suspended) with code {d}", .{code});
        },
        .Unknown => |code| {
            std.debug.print("Process ended with unknown termination code {d}", .{code});
        },
    }
}
