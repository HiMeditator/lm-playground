from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import Choice, ChoiceDelta, ChoiceDeltaToolCall, ChoiceDeltaToolCallFunction
from openai.types.completion_usage import CompletionUsage
from openai.types.completion_usage import CompletionTokensDetails, PromptTokensDetails

# 阿里云普通流式响应
# 注意实际返回中 "choices 非空" 和 "usage 非 None" 只会出现一种，这里合并到了一起
ChatCompletionChunk(
    id='chatcmpl-31f183c1-cc30-9f3d-a30e-856efbc9f86c',
    choices=[
        Choice(
            delta=ChoiceDelta(
                content='', 
                function_call=None, 
                refusal=None, 
                role='assistant', 
                tool_calls=None
            ), 
            finish_reason=None, 
            index=0, 
            logprobs=None
        )
    ],
    created=1770098240,
    model='qwen-plus',
    object='chat.completion.chunk', 
    service_tier=None, 
    system_fingerprint=None, 
    usage=CompletionUsage(
        completion_tokens=66, 
        prompt_tokens=21, 
        total_tokens=87, 
        completion_tokens_details=None, 
        prompt_tokens_details=PromptTokensDetails(
            audio_tokens=None, 
            cached_tokens=0
        )
    )
)

# 工具调用请求流式响应
# https://bailian.console.aliyun.com/cn-beijing/?tab=doc#/doc/?type=model&url=2862208
ChatCompletionChunk(
    id='chatcmpl-6ef3a298-0049-93c7-b3a3-4ce94b4f8daf', 
    choices=[
        Choice(
            delta=ChoiceDelta(
                content=None, 
                function_call=None, 
                refusal=None, 
                role='assistant', 
                tool_calls=[
                    ChoiceDeltaToolCall(
                        index=0, 
                        id='call_c382887ee8144df692c47d', 
                        function=ChoiceDeltaToolCallFunction(
                            arguments='{"', # 注意这里是流式返回的
                            name='get_atri_greet'
                        ),     
                        type='function'
                    )
                ]
            ), 
            finish_reason=None, 
            index=0, 
            logprobs=None
        )
    ], 
    created=1770100705, 
    model='qwen-plus', 
    object='chat.completion.chunk', 
    service_tier=None, 
    system_fingerprint=None, 
    usage=None
)


# OpenAI 普通流式响应
# 注意实际返回中 "choices 非空" 和 "usage 非 None" 只会出现一种，这里合并到了一起
ChatCompletionChunk(
    id='chatcmpl-D53iJGXxYbDHTGGAJIbofqZw42INU', 
    choices=[
        Choice(
            delta=ChoiceDelta(
                content='', 
                function_call=None, 
                refusal=None, 
                role='assistant', 
                tool_calls=None
            ), finish_reason=None, index=0, logprobs=None
        )
    ],
    created=1770098287, 
    model='gpt-4o-2024-08-06', 
    object='chat.completion.chunk', 
    service_tier='default', 
    system_fingerprint='fp_fa7f5b168b', 
    usage=CompletionUsage(
        completion_tokens=30, 
        prompt_tokens=19, 
        total_tokens=49, 
        completion_tokens_details=CompletionTokensDetails(
            accepted_prediction_tokens=0, 
            audio_tokens=0, 
            reasoning_tokens=0, 
            rejected_prediction_tokens=0
        ), 
        prompt_tokens_details=PromptTokensDetails(
            audio_tokens=0, 
            cached_tokens=0
        )
    ), 
    # obfuscation='U0ItOof6deGkN8H'
)
