用户使用的uv进行的python包管理以及相关运行操作，先执行 [activate] 命令 激活虚拟环境。 及使用uv pip install 进行相关安装操作

用户指定你需要进行git操作的时候，才进行撰写git提交记录，严格遵守Angular Commit Message Guidelines。

# 笛卡尔工程化工作法 + Python编码规范（用于FastAPI项目）

- 回答一律使用简体中文；编写/输出所有代码时统一使用英文。
- 不阿谀奉承；遇到用户不合理的想法或实现，直言不讳地指出并给出更优替代方案。
- 若信息不足无法精确推进，先明确缺口并向用户索取必要数据/上下文再继续。

## 技术与环境约束

- **技术栈**：FastAPI + Pydantic；uv 进行包管理与虚拟环境。
- **异步优先**：默认使用异步编程模式，I/O操作必须异步化；避免在异步上下文中调用同步阻塞操作。
- **运行约束**：运行任何 Python 相关命令前，先执行 activate 激活虚拟环境。
- **依赖抽象**：外部依赖（DB/Redis/HTTP/LLM等）通过异步适配器/接口抽象对接，便于替换与测试。

## 方法论：笛卡尔四原则（工程化落地）

### 1) 证据原则（Evidence）
- **明确验收标准**：输入/输出、边界条件、错误码、幂等与性能目标（含并发性能）。
- **异步契约先行**：先定义异步 Pydantic schema、类型提示（含 `Awaitable`）、断言与接口契约。
- **性能基线**：明确异步场景下的响应时间、吞吐量、并发数目标。
- **风险评估**：不确定时，列出假设与影响，选择风险最小的推进路径，确保可回滚。

### 2) 分析原则（Decomposition）
- **分层架构**：API 层 / 异步服务层 / 领域模型 / 异步基础设施（DB、Redis、HTTP、LLM）。
- **异步依赖倒置**：用异步构造器/依赖注入隔离外部系统，支持异步 mock 测试。
- **并发边界**：明确异步数据流与副作用边界，把外部交互收敛在异步适配器层。
- **资源隔离**：连接池、信号量等并发资源统一管理，避免资源竞争。

### 3) 综合原则（Synthesis）
- **异步骨架优先**：先实现最小异步正向路径（happy path）与可运行骨架。
- **渐进式完善**：再补齐异步异常处理、并发控制、背压机制。
- **小步集成**：保持模块边界清晰，异步组件可独立测试与替换。
- **性能优化**：识别并发瓶颈，合理使用 `asyncio.gather`、`asyncio.as_completed` 等。
- **详尽测试**：开发或者进行相关bug修复代码编写后，在tests文件夹撰写python或sh脚本进行测试确保正确完成任务。

### 4) 枚举原则（Enumeration）
- **异步复核清单**：
  - 边界输入与异步验证
  - 异步异常流与错误传播
  - 并发控制、背压与熔断
  - 异步超时/重试/幂等
  - 异步日志与可观测性（trace_id 跨异步调用链）
  - 连接池与异步资源管理
  - 异步性能基线与监控
- **异步测试覆盖**：异步单元/集成/负载测试，含并发竞态与资源泄漏检测。

## Python 异步编程规范（强制）

### 基础规范
- **PEP8 + 异步**：命名、缩进遵循 PEP8；异步函数明确 `async` 前缀。
- **设计原则**：异步版 SOLID 原则；职责单一、异步依赖倒置、组合优先于继承。
- **类型提示**：所有异步函数显式标注 `async def` 与返回类型；使用 `Awaitable[T]`、`AsyncIterator[T]` 等。

### 异步核心约定
```python
# ✅ 正确：异步函数签名
async def fetch_user_data(user_id: int) -> UserResponse:
    """异步获取用户数据"""
    pass

# ✅ 正确：异步依赖注入
async def get_async_db() -> AsyncIterator[AsyncSession]:
    """异步数据库会话"""
    pass

# ❌ 错误：在异步函数中调用同步阻塞操作
async def bad_example():
    time.sleep(1)  # 阻塞整个事件循环
```

### 异步错误处理
- **超时控制**：所有异步 I/O 设置 `asyncio.timeout` 或 `asyncio.wait_for`。
- **重试机制**：使用异步重试库（如 `tenacity`）实现指数退避+抖动。
- **并发限制**：用 `asyncio.Semaphore` 控制并发数，防止资源耗尽。
- **优雅降级**：异步熔断、回源与降级策略。
- **异常传播**：异步异常栈保留完整上下文，便于调试。

### 异步资源管理
```python
# ✅ 异步上下文管理器
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()

# ✅ 异步连接池管理
async with async_db_pool.get_connection() as conn:
    result = await conn.execute(query)
```

### 异步并发模式
```python
# ✅ 并发执行多个异步任务
results = await asyncio.gather(
    fetch_user(1),
    fetch_user(2),
    fetch_user(3),
    return_exceptions=True  # 异常隔离
)

# ✅ 流式处理大量数据
async for item in async_data_stream():
    await process_item(item)
```

## FastAPI 异步约定

### 路由层异步化
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    """异步路由处理"""
    return await user_service.get_user(user_id)
```

### 异步依赖注入
```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """异步依赖解析"""
    return await auth_service.verify_token(token)
```

### 异步中间件
```python
@app.middleware("http")
async def async_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 统一异步错误处理
- 输入/输出统一使用 Pydantic models，异步验证与错误映射。
- 异步服务层纯粹、无框架耦合；外部依赖通过异步接口与适配器层实现。
- 统一异步错误响应格式与错误码；对调用方保持稳定契约。

## 异步调试与可观测性

### 异步日志规范
- 使用结构化异步日志，trace_id 跨异步调用链传播
- 关键异步操作记录开始/完成/失败状态，含耗时与上下文

### 异步性能监控
- **关键指标**：异步响应时间、并发数、队列深度、连接池利用率
- **链路跟踪**：跨异步调用的 trace_id 传播与上下文保持
- **资源监控**：检测协程泄漏、连接池耗尽、事件循环阻塞

## 异步工作流（从需求到交付）

1. **需求澄清与验收**：列出异步场景的性能、并发、错误处理目标；不足则向用户提问补全。

2. **异步契约先行**：先写异步 schema 与接口签名（含异步类型提示），再实现最小异步正向路径。

3. **异步实现与加固**：
   - 补齐异步异常/边界/补偿逻辑
   - 添加超时、重试、并发控制
   - 增加异步日志与度量

4. **异步质量校验**：ruff、类型检查、pytest（含异步测试、并发竞态测试）；全部通过再提交。

5. **异步交付说明**：简述异步实现要点、性能基线、并发策略、监控方式与后续优化事项。

## 异步评审清单（提交前自检）

- [ ] **异步契约**：异步函数签名是否明确？类型提示是否包含 `Awaitable`？
- [ ] **并发安全**：是否正确使用异步锁、信号量？避免竞态条件？
- [ ] **资源管理**：异步资源是否正确释放？连接池配置是否合理？
- [ ] **错误处理**：异步超时/重试/熔断是否完整？异常传播是否清晰？
- [ ] **性能优化**：是否识别并优化异步瓶颈？合理使用 `gather`、`as_completed`？
- [ ] **可观测性**：异步日志是否足以定位问题？trace_id 是否正确传播？
- [ ] **测试覆盖**：异步单元/集成/负载测试是否充分？本地 ruff 与测试是否均为绿色？

## 互动原则

- 信息不足则先提问而非盲目实现；明确异步场景的假设与权衡。
- 对不合理的同步阻塞方案直言指出，给出异步替代路径（含性能对比与迁移成本）。
- 保持产出可运行、可测试、可维护的异步代码，优先最小可用且可增量扩展的异步实现。
- **异步优先原则**：除非有明确的同步需求，否则默认推荐异步实现方案。


