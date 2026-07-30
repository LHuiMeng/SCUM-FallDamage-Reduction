# SCUM Fall Damage Reduction Mod

将玩家坠落/着地伤害减少至原版的 **30%**。极限高度坠落从即死变为只掉 30% 血量。

## 效果

| 坠落高度 | 原版伤害 | 修改后(×0.3) |
|---------|---------|-------------|
| ≤ 10层楼 (速度 ≤ 950) | **0** 安全 | **0** 安全 |
| 15层楼 (速度 ≈ 1400) | ≈53 半血 | ≈16 |
| 极限坠落 (速度 = 1800) | **100** 即死 | **30** |

## 安装

1. 下载 `SCUM_FallDamage_Reduction.pak`
2. 放入 `SCUM\Saved\Mods\` 目录
3. 启动游戏/重启服务器

**服务端部署**：放入服务端 `SCUM/Saved/Mods/`，设置 `bSyncModsToClients=True` 自动同步。

## 技术原理

修改 `Characters/Prisoner/Curves/Landing/` 下的两条 CurveFloat 资产：
- `LandingDamagePrepared` — 准备着地（按住跳跃键缓冲落地）
- `LandingDamageUnprepared` — 无准备着地（直接自由落体）

两条曲线原本在速度 1800 时伤害值为 100（即死），现统一降至 30（×0.3）。
曲线在速度 0~950 范围内保持 0 伤害（安全高度不变）。

## 文件结构

```
SCUM/Content/ConZ_Files/Characters/Prisoner/Curves/Landing/
├── LandingDamagePrepared.uasset  (modified)
├── LandingDamagePrepared.uexp    (modified)
├── LandingDamageUnprepared.uasset (modified)
└── LandingDamageUnprepared.uexp   (modified)
```

## 自行构建

```bash
# 需要: dotnet SDK + UAssetCLI + repak
python build_fall_damage_mod.py
```

## 兼容性

- ✅ 纯 PAK 数据覆盖，不修改二进制
- ✅ UAssetCLI 完整 round-trip，序列化兼容
- ✅ 服务端/客户端均可使用
- ✅ 不影响其他伤害系统
